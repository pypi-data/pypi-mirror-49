from __future__ import print_function
from aim.engine.aim_model import AimModel
# import docker
import os

"""
    Deploys to docker as a docker api...
    all docker functionality is here
"""


class DockerDeploy():
    def __init__(self, model_path):
        self.model_path = model_path

    def _model_dest_name(self):
        """ Return dest and name of model """
        # TODO: perform all sorts of checks here
        dest, name = os.path.split(self.model_path)
        name = ''.join(i for i in name.split('.')[0:-1])
        return (dest, name)

    def set_img_name(self, name):
        # TODO: organize random name
        self.image_name = name
        return self

    def set_img_version(self, version):
        # TODO: set latest if no version is provided
        self.image_version = version
        return self

    def build_image(self):
        dest, name = self._model_dest_name()
        image_tag = self.image_name + ':' + self.image_version
        am = AimModel.load_model(dest, name)
        print(am.framework())
        # context_path = os.path.dirname(os.path.realpath(__file__))
        # client = docker.from_env()
        # build_params = {
        #     'path': context_path,
        #     'tag': image_tag,
        #     'quiet': False
        # }
        # docker_build = client.images.build(**build_params)
        # for line in docker_build[1]:
        #     # time.sleep(1)
        #     print(line)
        return image_tag


class DockerFilePaths():
    def __init__(self):
        pass
