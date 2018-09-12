import docker
from flask.json import jsonify

from webapp import app
from webapp.json_api import json_api, serializers


@app.route('/containers/<string:container_id>', methods=["GET"])
@json_api
def container_get(container_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return jsonify({"error": "No container found"}), 404
    fields = ["id", "image", "name", "short_id", "status"]
    return jsonify(serializers.dict_serializer(container, fields=fields))


@app.route("/containers/<string:container_id>/logs", methods=["GET"])
@json_api
def container_log_get(container_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return jsonify({"error": "No container found."}), 404
    fields = ["id", "image", "name"]
    serialized_container = serializers.dict_serializer(container, fields=fields)
    serialized_container['logs'] = container.logs().decode('utf-8')
    return jsonify(serialized_container)
