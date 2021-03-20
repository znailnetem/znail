import functools
import types

import flask
import flask_cors
import flask_restplus

app = flask.Flask("znail", static_folder="ui/web/static", template_folder="ui/web/templates")
flask_cors.CORS(app)
api = flask_restplus.Api(version="1.0", title="Znail", default="Znail", default_label="", doc="/api/swagger")


def lazy_api_initialization_wrapper(app, api):
    app_run = app.run
    app_test_client = app.test_client

    @functools.lru_cache(maxsize=1)
    def init_app():
        api.init_app(app)

    def run_wrapper(*args, **kwargs):
        init_app()
        return app_run(*args, **kwargs)

    def test_client_wrapper(*args, **kwargs):
        init_app()
        return app_test_client(*args, **kwargs)

    app.run = run_wrapper
    app.test_client = test_client_wrapper


# flask-resplus overrides the default route if it is initialized before it is:
# https://github.com/noirbizarre/flask-restplus/issues/247
#
# Znail registers its routes lazily, at import time.
# This wrapper delays the initialization of flask_restplus until all imports are done.
lazy_api_initialization_wrapper(app, api)


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


api.route = types.MethodType(api_route, api)
