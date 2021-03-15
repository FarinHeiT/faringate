import inspect
import os
from jinja2 import Environment, FileSystemLoader
from webob import Request, Response
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter


class AppFactory:
    def __init__(self, templates_dir='templates'):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))



    def __call__(self, environ, start_response):
        
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)


    def add_route(self, route, handler):
        assert route not in self.routes, "Route already exists"
        
        self.routes[route] = handler


    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper



    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found"

    
    def get_handler(self, request_route):
        for path, handler in self.routes.items():
            parse_params = parse(path, request_route)
            if parse_params:
                return handler, parse_params.named
        
        return None, None


    def handle_request(self, request):
        response = Response()
        
        handler, params = self.get_handler(request.path)

        if handler:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if not handler:
                    raise AttributeError("Method not allowed", request.method)
            
            handler(request, response, **params)
        else:
            self.default_response(response)

        return response
        
    
    def test_client(self, base_url='http://testserv'):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session


    def template(self, template_name, context=None):
        context = context if context else {}

        return self.templates_env.get_template(template_name).render(**context)
    

