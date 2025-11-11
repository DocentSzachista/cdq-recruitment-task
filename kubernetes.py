from jinja2 import Environment, FileSystemLoader


class Manifest:
    """Base class for kubernetes manifest generation program"""

    dirpath = "manifests"
    template = str()
    required_args = set()

    def __init__(self, args: dict):
        if type(self) is Manifest:
            raise TypeError("Cannot instantiate Manifest directly, use a subclass instead")
        self._environment = Environment(loader=FileSystemLoader(self.dirpath), trim_blocks=True)
        self._args = args
        self._check_args()

    def _check_args(self):
        """Valides if all of the required arguments for the manifest has been supplied"""
        missing_args = self.required_args - self._args.keys()
        if missing_args:
            raise ValueError(f"Required arguments are missing: {', '.join(missing_args)}")

    def produce_manifest(self):
        """Generates kubernetes manifest from the file placed in manifests directory."""
        template = self._environment.get_template(self.template)
        return template.render(**self._args)


class Pod(Manifest):

    template = "pod.yaml.j2"
    required_args = {"name", "image"}


class Deployment(Pod):

    template = "deployment.yaml.j2"
