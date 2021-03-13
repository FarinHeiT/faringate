from webob import Request, Response
from parse import parse

class AppFactory:
    def __init__(self):
        self.routes = {}


    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)


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
            handler(request, response, **params)
        else:
            self.default_response(response)

        return response
        