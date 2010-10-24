#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Wojciech 'KosciaK' Pietrzok
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = "Wojciech 'KosciaK' Pietrzok (kosciak@kosciak.net)"
__version__ = "0.2"


import logging
import traceback
import sys

from google.appengine.ext.webapp.util import run_wsgi_app

import pesto

from routes import Mapper, URLGenerator

from jinja2 import Environment, Template


Request = pesto.request.Request


class Response(pesto.Response):

    def set_content(self, content):
        return self.replace(content=[content])

    def clear(self):
        return self.replace(content=[])


class RequestHandler(object):

    env = Environment() # TODO: complete

    def __init__(self, url_generator):
        self.get_url = url_generator

    def render(self, template, context={}, status=200, headers=None, **kwargs):
        if not isinstance(template, Template):
            template = env.get_template(template)
        content = template.render(context).encode('utf-8')
        return Response([content], status, headers, **kwargs)

    def redirect(self, location, status=302):
        return Response.redirect(location, status)

    def error(self, status=500, content=[], headers=None, **kwargs):
        return Response(content, status, headers, **kwargs)

    def handle_exception(self, exception, stream):
        print >> stream, exception
        print >> stream, ''.join(traceback.format_exception(*sys.exc_info()))
        return self.error(500)


class RoutesDispatcher(object):

    def __init__(self, mapper):
        self.mapper = mapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)

    def dispatch(self, request):
        url_generator = URLGenerator(self.mapper, request.environ)
        kwargs, route = self.mapper.routematch(request.path_info) or ({}, None)
        if route and route.redirect:
            logging.warning('REDIRECTING!')
            route_name = '_redirect_%s' % id(route)
            location = url_generator(route_name, **kwargs)
            '''
            start_response(route.redirect_status, 
                           [('Content-Type', 'text/plain; charset=utf8'), 
                            ('Location', location)])
            return []
            '''
            return Response.redirect(location, status=route.redirect_status)
        if not kwargs:
            # TODO: exception? 404_handler?
            pass
        handler = kwargs.pop('controller')(url_generator)
        action_name = kwargs.pop('action', None)
        if not action_name:
            action_name = request.request_method.lower()
        try:
            action = getattr(handler, action_name)
            return action(request, **kwargs)
        except Exception, e:
            return handler.handle_exception(e, request.environ['wsgi.errors'])


class TestHandler(RequestHandler):
        
    def get(self, request, foo="World"):
        env = ''
        for key, value in request.environ.items():
            env += '%s = %s<br />' % (key, value)
        template = Template('<h1>Hello {{ foo }}!</h1><p>{{env}}</p>')
        #raise ValueError('!!!!!!!!')
        return self.render(template, {'foo': foo, 'env':env})
        #response = Response()
        #response = response.set_content(env)
        #return response.clear()



map = Mapper()
map.connect("index", "/", controller=TestHandler, )
map.connect("/{foo}", controller=TestHandler, )
map.redirect("/{foo}/{id:\d+}", "/{foo}")

dispatcher = RoutesDispatcher(map)

application = dispatcher

def main():
    # Run as pesto_app:
    #application = pesto.to_wsgi(dispatcher.dispatch)
    # Run as wsgi_app:
    run_wsgi_app(application)


if __name__ == '__main__':
    main()


