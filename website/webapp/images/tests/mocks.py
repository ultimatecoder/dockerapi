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
