import argparse
from kubernetes import Deployment, Pod
import re

RFC_1123 = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'
LABELS_REGEX = r'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'
ENV_NAME_REGEX=r"[A-Za-z_][A-Za-z0-9_]*"


def prepare_parser():
    parser = argparse.ArgumentParser(
        description="Program that basing on provided arguments generates Kubernetes yaml manifests."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_deployment_subparser(
        subparsers.add_parser("deployment", description="Kubernetes Deployment manifest")
    )
    prepare_pod_subparser(
        subparsers.add_parser("pod", description="Kubernetes Pod manifest")
    )

    return parser.parse_known_args()[0]


def prepare_metadata_arguments(parser: argparse.ArgumentParser) -> None:

    parser.add_argument(
        "--name", type=validate_k8s_name, required=True,
        help="Resource name (required)"
    )
    parser.add_argument(
        "--labels", type=parse_label,
        help="Labels describing resource, coma-separated provided in <label_name>=<label_value>"
    )

def prepare_container_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--envs", type=parse_env,
        help="List of environment variables that should be added to the container provided comma separated in <env_name>=<env_value> manner"
    )

    parser.add_argument(
        "--image", type=str, required=True,
        help="Docker image that the container should use (required)"
    )

def prepare_deployment_subparser(parser: argparse.ArgumentParser):

    prepare_metadata_arguments(parser)
    prepare_container_arguments(parser)
    parser.add_argument(
        "--replicas", type=int, default=3,
        help="Number of pod replicas that Kubernetes deployment will create. Defaults to 3"
    )


def prepare_pod_subparser(parser: argparse.ArgumentParser):

    prepare_metadata_arguments(parser)
    prepare_container_arguments(parser)


def validate_k8s_name(
        value: str
    ):
    pattern = re.compile(RFC_1123)
    result = pattern.fullmatch(value)
    if not result:
        raise argparse.ArgumentTypeError(f"Invalid name {value}: must match DNS-1123 label pattern")
    if "." in value:
        raise argparse.ArgumentTypeError(f"Invalid value for container name {value}: must not contain dots.")
    if len(value) > 63:
        raise argparse.ArgumentTypeError("Resource name must not exceed 63 characters.")
    return value

def parse_env(env_string: str):
    return parse_coma_values(env_string, False)

def parse_label(env_string: str):
    return parse_coma_values(env_string, True)

def parse_coma_values(env_string: str, is_label: bool):
    return_dict = {}

    parser = re.compile( LABELS_REGEX if is_label else ENV_NAME_REGEX )

    for pair in env_string.split(","):
        if "=" not in pair:
            raise argparse.ArgumentTypeError(f"Invalid format '{pair}'. Expected '<key>=<value>'")
        key, value = pair.split("=", 1)
        key, value = key.strip(), value.strip()
        if not key or not value:
            raise argparse.ArgumentTypeError(f"Empty key, or value in {pair}. Expected '<key>=<value>'")
        if not parser.fullmatch(key):
            raise argparse.ArgumentTypeError(f"Key name of the resource is not valid {key}")
        if (not parser.fullmatch(value)) and is_label:
            raise argparse.ArgumentTypeError(f"value of the resource is not valid {value}")
        return_dict[key] = value
    return return_dict


if __name__ == "__main__":
    args = vars(prepare_parser())
    command = args.pop("command")
    if command == "deployment":
        resource = Deployment(args)
    if command == "pod":
        resource = Pod(args)
    print(resource.produce_manifest())

