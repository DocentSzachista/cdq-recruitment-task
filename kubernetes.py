from abc import abstractmethod, ABC
from jinja2 import Environment, FileSystemLoader


class Manifest(ABC):
    dirpath = "manifests"

    @abstractmethod
    def produce_manifest(self):
        """Generates kubernetes manifest from the file placed in manifests directory."""
        return

    def _parse_attributes(self, args: dict):
        """Performs attributes checks if they are provided correct way"""
        for key in self.expected_args:
            setattr(self, key, args.get(key, {}))


class Deployment(Manifest):

    expected_args = {"name", "envs", "replicas", "labels"}

    def __init__(self, args):
        self.environment = Environment(loader=FileSystemLoader(self.dirpath))
        self.args = args


    def produce_manifest(self):
        template = self.environment.get_template("deployment.yaml.j2")
        return template.render(
            {
                "name": self.args['name'],
                "replicas": self.args['replicas'],
                "labels": self.args['labels'],
                "envs": self.args['envs'],
            }
        )