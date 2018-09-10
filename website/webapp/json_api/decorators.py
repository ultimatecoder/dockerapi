from functools import wraps

from flask import request
from flask.json import jsonify


def json_api(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if (
            request.method in ["POST", "PUT"] and
            request.headers.get("Content-type") != "application/json"
        ):
            return jsonify({"error": "Unsupported Content type"}), 400
        if request.accept_mimetypes.find("application/json") == -1:
            return jsonify({"error": "Unsupported Media type"}), 415
        return f(*args, **kwargs)

    return wrapper
