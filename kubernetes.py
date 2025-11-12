from jinja2 import Environment, FileSystemLoader


class Manifest:
    """Base class for kubernetes manifest generation program"""

    dirpath = "manifests"
    template = str()
    required_args = set()
    default_args_values = dict()

    def __init__(self, args: dict) -> None:
        if type(self) is Manifest:
            raise TypeError("Cannot instantiate Manifest directly, use a subclass instead")
        self._environment = Environment(loader=FileSystemLoader(self.dirpath), trim_blocks=True)
        self._args = args
        self._check_args()

    def _check_args(self) -> None:
        """Valides if all of the required arguments for the manifest has been supplied
           and adds args default values
        """
        missing_args = self.required_args - self._args.keys()
        if missing_args:
            raise ValueError(f"Required arguments are missing: {', '.join(missing_args)}")
        for key, value in self.default_args_values.items():
            self._args.setdefault(key, value)

    def produce_manifest(self) -> str:
        """Generates kubernetes manifest from the file placed in manifests directory."""
        template = self._environment.get_template(self.template)
        return template.render(**self._args)


class Pod(Manifest):

    template = "pod.yaml.j2"
    required_args = {"name", "image"}



class Deployment(Pod):
    default_args_values = {"replicas": 3}
    template = "deployment.yaml.j2"
