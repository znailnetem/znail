import flask
import flask_restplus

from znail.ui import api

json_request_model = api.model("JsonRequest", {"message": flask_restplus.fields.String})


def json_request_handler(schema=None, model=None):
    def decorator(action):
        @api.expect(model)
        @api.response(200, "Success", json_request_model)
        @api.response(400, "No input data provided", json_request_model)
        @api.response(422, "Input validation error", json_request_model)
        @api.response(500, "Internal server error", json_request_model)
        def wrapper(*args, **kwargs):
            return handle_json_request(schema, action, *args, **kwargs)

        return wrapper

    return decorator


def handle_json_request(schema, action, *args, **kwargs):
    json_data = flask.request.get_json()
    if schema and not json_data:
        return {"message": "No input data provided"}, 400

    if schema:
        data, errors = schema.load(json_data)
        if errors:
            return {"message": str(errors)}, 422
    else:
        data = None

    try:
        action(*args, data=data, **kwargs)
    except Exception as e:
        return {"message": str(e)}, 500

    return {"message": "ok"}, 200


class _NoneAttributes:
    def __getattribute__(self, attr):
        return None


NoneAttributes = _NoneAttributes()
