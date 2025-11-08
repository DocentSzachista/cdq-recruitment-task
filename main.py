import argparse
from kubernetes import Deployment


def prepare_parser():
    parser = argparse.ArgumentParser(
        description="Program that basing on provided arguments generates Kubernetes yaml manifest describing Deployment")
    parser.add_argument("--name", type=str, required=True, help="Container and resource name")
    parser.add_argument("--labels", type=parse_coma_values, help="Labels describing deployment, coma-separated provided in <label_name>=<label_value>")
    parser.add_argument("--replicas", type=int, default=3, help="Number of pod replicas that Kubernetes deployment will create. Defaults to 3")
    parser.add_argument("--envs", type=parse_coma_values, help="List of environment variables that should be added to the container provided comma separated in <env_name>=<env_value> manner")
    parser.add_argument("--image", type=str, required=True, help="Docker image that the container should use")
    return parser.parse_known_args()[0]


def parse_coma_values(env_string: str):
    return_dict = {}
    for env in env_string.split(","):
        key, value = env.split("=")
        return_dict[key] = value
    return return_dict


if __name__ == "__main__":
    args = vars(prepare_parser())
    deplo = Deployment(args)
    print( deplo.produce_manifest() )

