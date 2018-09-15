import docker
from flask import request
from flask.json import jsonify

from webapp import app
from webapp.json_api import json_api, serializers


@app.route(
    '/containers/<string:container_id>', methods=["GET"], strict_slashes=False
)
@json_api
def container_get(container_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return jsonify({"error": "No container found"}), 404
    fields = ["id", "image", "name", "short_id", "status"]
    return jsonify(serializers.dict_serializer(container, fields=fields))


@app.route(
    "/containers/<string:container_id>/logs",
    methods=["GET"],
    strict_slashes=False
)
@json_api
def container_log_get(container_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return jsonify({"error": "No container found."}), 404
    serialized_container = serializers.dict_serializer(
        container, fields=["id", "image", "name"]
    )
    serialized_container['logs'] = container.logs().decode('utf-8')
    return jsonify(serialized_container)


@app.route("/containers", methods=["GET"], strict_slashes=False)
@json_api
def containers_get():
    response = {"data": []}
    client = docker.from_env()
    all = not request.args.get("active", False)
    for container in client.containers.list(all=all):
        dict_container = serializers.dict_serializer(
            container, fields=["id", "image", "name", "short_id", "status"]
        )
        response["data"].append(dict_container)
    return jsonify(response)


@app.route(
    "/containers/<string:container_id>",
    methods=["DELETE"],
    strict_slashes=False
)
@json_api
def container_delete(container_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return jsonify({"error": "No container found"}), 404
    container.remove()
    return jsonify({"message": "Container removed successfully."})


@app.route(
    "/containers/<string:container_id>",
    methods=["PATCH"],
    strict_slashes=False
)
@json_api
def container_update(container_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return jsonify({"error": "No container found"}), 404
    request_data = request.get_json() or {}
    desired_state = request_data.get('state', '').lower()
    if desired_state not in ['start', 'stop']:
        return jsonify({"error": "API parameter 'state' is required."}), 400
    operation = getattr(container, desired_state)
    operation()
    return jsonify({"message": f"Container {desired_state} successfully!"})


@app.route("/containers", methods=["POST"], strict_slashes=False)
@json_api
def container_create():
    client = docker.from_env()
    request_data = request.get_json()
    image = request_data.get('image')
    command = request_data.get("command", "")
    ports = request_data.get("ports", {})
    if not image:
        return jsonify({"error": "Parameter 'image' is required"}), 400
    elif image and type(image) is not str:
        return jsonify({
            "error": "Parameter 'image' should be type 'str'"
        }), 400
    elif type(command) not in [str, list]:
        return jsonify({
            "error": (
                "Invalid command parameter. "
                "It should be either type 'str' or 'list'"
            )
        }), 400
    elif type(ports) != dict:
        return jsonify({
            "error": (
                "Invalid 'ports' value. "
                "It should be valid Javascript Object."
            )
        }), 400
    try:
        container = client.containers.run(
            image, command, ports=ports, detach=True
        )
    except docker.errors.ContainerError as e:
        return jsonify({"error": e.message}), 400
    except docker.errors.ImageNotFound as e:
        return jsonify({"error": f"Image {image} not found"}), 400
    serialized_container = serializers.dict_serializer(
        container, fields=["id", "image", "name", "short_id", "status"]
    )
    return jsonify(serialized_container), 201
