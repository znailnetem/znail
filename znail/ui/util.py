import flask


def handle_json_request(schema, action):
    json_data = flask.request.get_json()
    if schema and not json_data:
        return {'message': 'No input data provided'}, 400

    if schema:
        data, errors = schema.load(json_data)
        if errors:
            return {'message': str(errors)}, 422
    else:
        data = None

    try:
        action(data)
    except Exception as e:
        return {'message': str(e)}, 500

    return {'message': 'ok'}, 200


class _NoneAttributes(object):

    def __getattribute__(self, attr):
        return None


NoneAttributes = _NoneAttributes()
