import docker
from flask import request
from flask.json import jsonify

from webapp import app
from webapp.json_api import json_api, serializers


@app.route('/images', methods=["GET"])
@json_api
def images_get():
    client = docker.from_env()
    response = {"data": []}
    for image in client.images.list():
        _image = serializers.dict_serializer(
            image, fields=["id", "short_id", "tags"]
        )
        response["data"].append(_image)
    return jsonify(response)


@app.route("/images", methods=["POST"])
@json_api
def images_post():
    request_data = request.get_json()
    if not request_data:
        return jsonify({
            "error": "No request body found"
        }), 400
    if request_data and "name" not in request_data:
        return jsonify({
            "error": "Requst body param 'name' is required"
        }), 400
    client = docker.from_env()
    image = client.images.pull(request_data["name"])
    response = serializers.dict_serializer(
        image, fields=["id", "short_id", "tags"]
    )
    return jsonify(response), 201


@app.route("/images/<string:image_id>", methods=["GET"])
@json_api
def images_individual_get(image_id):
    client = docker.from_env()
    try:
        image = client.images.get(image_id)
    except docker.errors.ImageNotFound as e:
        return jsonify({
            "error": "Image not found."
        }), 404
    response = serializers.dict_serializer(
        image, fields=["id", "short_id", "tags"]
    )
    return jsonify(response)


@app.route("/images/<string:image_id>", methods=["DELETE"])
def images_individual_delete(image_id):
    client = docker.from_env()
    try:
        client.images.remove(image_id)
    except docker.errors.ImageNotFound as e:
        return jsonify({
            "error": "Image not found."
        }), 404
    return jsonify({
        "message": f"Image {image_id} deleted successfully"
    })
