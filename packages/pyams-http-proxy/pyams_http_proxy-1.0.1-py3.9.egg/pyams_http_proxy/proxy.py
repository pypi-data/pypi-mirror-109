#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_http_proxy.proxy module

This module defines the main proxy application.
"""

__docformat__ = 'restructuredtext'

import importlib
import logging
from urllib.parse import urlsplit

import httpx
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse


LOGGER = logging.getLogger('PyAMS (proxy)')


class ProxyApplication:
    """Starlette proxy handler"""

    def __init__(self, config):
        self.config = config
        plugins = self.plugins = {}
        for key, names in config['plugins'].items():
            pkg, klass = names.split()
            try:
                module = importlib.import_module(pkg)
                plugin = plugins[key] = getattr(module, klass)
                plugin.init_plugin()
            except ImportError:
                LOGGER.warning("Can't import plug-in package: %s", pkg)
            except AttributeError:
                LOGGER.warning("Can't load plug-in: %s", klass)
        remotes = self.remotes = {}
        for remote in config['remotes']:
            for base_path, settings in remote.items():
                remotes[base_path] = {
                    'remote': settings['remote'],
                    'config': settings.get('config', {}),
                    'timeout': settings.get('timeout', 5.0) or None
                }
                for plugin_name in settings.get('plugins', ''):
                    plugin = plugins.get(plugin_name)
                    if plugin is not None:
                        plugin.init_proxy(base_path, settings)
                        remotes[base_path].setdefault('plugins', []).append(plugin)
        self.client = httpx.AsyncClient(verify=config.get('ssl_certificates', None))

    async def __call__(self, scope, receive, send):
        """Async proxy call"""
        if scope['type'] == 'http':
            request = Request(scope, receive=receive)
            config = self.get_config(request)
            plugins_config = config.get('config', {})
            for plugin in config.get('plugins', ()):
                if hasattr(plugin, 'pre_handler') and \
                        plugin.apply_to(request, plugins_config[plugin.config_name]):
                    request = await plugin.pre_handler(request,
                                                       plugins_config[plugin.config_name])
            async with self.client.stream(method=self.get_method(request),
                                          url=self.get_url(request),
                                          headers=self.get_headers(request),
                                          params=self.get_params(request),
                                          data=self.get_body(request),
                                          timeout=config.get('timeout'),
                                          allow_redirects=False) as response:
                for plugin in config.get('plugins', ()):
                    if hasattr(plugin, 'post_handler') and \
                            plugin.apply_to(request, plugins_config[plugin.config_name]):
                        response = await plugin.post_handler(request, response,
                                                             plugins_config[plugin.config_name])
                if isinstance(response, Response):
                    app = response
                else:
                    app = StreamingResponse(status_code=response.status_code,
                                            headers=response.headers,
                                            content=response.aiter_raw())
                await app(scope, receive, send)

        elif scope['type'] == 'lifespan':
            message = await receive()
            assert message['type'] == 'lifespan.startup'

            async with httpx.AsyncClient() as self.client:
                await send({'type': 'lifespan.startup.complete'})
                message = await receive()

            assert message['type'] == 'lifespan.complete'
            await send({'type': 'lifespan.shutdown.complete'})

    def get_config(self, request):
        """Request config getter"""
        path = request.url.path[1:].split('/')
        try:
            return self.remotes[path[0]]
        except KeyError as exc:
            raise HTTPException(404) from exc

    @staticmethod
    def get_method(request):
        """Request method getter"""
        return request.method

    def get_url(self, request):
        """Request remote URL getter"""
        components = urlsplit(self.get_config(request)['remote'])
        path = request.url.path[1:].split('/')
        return str(request.url.replace(scheme=components.scheme,
                                       netloc=components.netloc,
                                       path='/{}'.format('/'.join(path[1:]))))

    @staticmethod
    def get_headers(request, decode=False):
        """Request headers getter"""
        if decode:
            return [
                (key.decode(), value.decode())
                for key, value in request.headers.raw
                if key != b'host'
            ]
        return [
            (key, value)
            for key, value in request.headers.raw
            if key != b'host'
        ]

    @staticmethod
    def get_params(request, decode=False):
        """Request params getter"""
        if decode:
            return [
                (key.decode(), value.decode())
                for key, value in request.query_params.items()
            ]
        return [
            (key, value)
            for key, value in request.query_params.items()
        ]

    @staticmethod
    def get_body(request):
        """Request body getter"""
        if 'content-length' in request.headers or 'transfer-encoding' in request.headers:
            return request.stream()
        return None
