"""
    Deploys to docker as a docker api...
    all docker functionality is here
"""


class DockerDeploy():
    def __init__(self, model_path):
        self.model_path = model_path

    def create_image(self):
        print("Create Image!!!!")
