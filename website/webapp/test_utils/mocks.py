from unittest.mock import MagicMock

import docker


DockerClient = MagicMock(docker.client.DockerClient)


from_env = MagicMock(docker.from_env)
from_env.return_value = DockerClient


Images = []
for i in range(4):
    _i = MagicMock(docker.models.images.Image)
    _i.id = i
    _i.short_id = f"short_id {i}"
    _i.tags = [f"Image{i}:latest"]
    Images.append(_i)


ImageNotFound = MagicMock(
    side_effect=docker.errors.ImageNotFound('Image Doesnt exists')
)


Containers = []
for i in range(4):
    _i = MagicMock(docker.models.containers.Container)
    _i.id = i
    _i.image = f"image_{i}"
    _i.name = f"container_{i}"
    _i.short_id = f"short_id {i}"
    _i.status = "Up" if i % 2 else "Down"
    Containers.append(_i)


SingleContainer = MagicMock(return_value=Containers[0])


NotFound = MagicMock(
    side_effect=docker.errors.NotFound("Container didn't find")
)
