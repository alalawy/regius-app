name = "regius"

from webob import Request, Response
from parse import parse
import inspect
import os
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
import gunicorn.app.base
from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Regius:

    def __init__(self, templates_dir="templates", static_dir="static"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(templates_dir))
        self.wsgi_app = WhiteNoise(self.wsgi_app, root=static_dir, autorefresh=True, max_age=1)
        

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


    def link(self, path):
        if path in self.routes:
            raise AssertionError("Such route already exists.")

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def add_link(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler
        
    
    def handle_request(self, request):

        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method now allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None


    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def template(self, template_name, data=None):
        if data is None:
            data = {}

        return self.templates_env.get_template(template_name).render(**data)

    def serve(self, address, port):
        options = {
            'bind': '%s:%s' % (address, port),
            'debug': True,
        }
        RegiusRun(self.wsgi_app, options).run()

    def redirect(self, req, resp, url):
        host = req.host_url
        resp.text = "<script> window.location.replace('"+host+url+"'); </script>"


class RegiusRun(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

