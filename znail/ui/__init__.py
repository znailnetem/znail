import types

import flask
import flask_cors
import flask_restful

app = flask.Flask('znail', static_folder='ui/web/static', template_folder='ui/web/templates')
flask_cors.CORS(app)
api = flask_restful.Api(app)


def api_route(self, *args, **kwargs):

    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


api.route = types.MethodType(api_route, api)
