# Kubernetes Deployment Manifest Generator
[![Kubernetes Manifests generation CI](https://github.com/DocentSzachista/cdq-recruitment-task/actions/workflows/CI.yaml/badge.svg?branch=master)](https://github.com/DocentSzachista/cdq-recruitment-task/actions/workflows/CI.yaml)
![Python](https://img.shields.io/badge/python-3.10-blue)


This Python project generates Kubernetes Deployment manifests from command-line arguments using Jinja2 templates.

## Features

- Validate Kubernetes resource names, labels, and environment variable names.
- Support for specifying replicas, labels, and environment variables.
- Generate YAML manifests for Kubernetes `Deployment` objects.
- Easy to extend for other Kubernetes resources using the base `Manifest` class.

## Installation

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

For running tests:
```bash
pip install -r requirements_test.txt
```

## Arguments

| Argument     | Required | Default | Description |
|-------------|----------|---------|-------------|
| `--name`    | Yes      | –       | Name of the deployment and container. Must follow DNS-1123 naming rules. |
| `--image`   | Yes      | –       | Docker image to use for the container. |
| `--replicas`| No       | 3       | Number of pod replicas the deployment will create. |
| `--labels`  | No       | –       | Comma-separated key=value pairs to label the deployment. |
| `--envs`    | No       | –       | Comma-separated environment variables for the container in VAR=value format. |

## Example usage

```bash
python main.py \
  --name my-app \
  --image nginx:latest \
  --replicas 2 \
  --labels app=myapp,env=dev \
  --envs DEBUG=True,LOG_LEVEL=info
```


## How to contribute/extend project

To add support for new Kubernetes resources or customize existing functionality, follow these steps:

1. **Create a Jinja2 Template**
   - Add a new template file in the `manifests/` folder, for example `service.yaml.j2`.
   - Use Jinja2 syntax to define placeholders for arguments that will be passed from Python.

2. **Create a Subclass of `Manifest`**
   - Open `kubernetes.py`.
   - Create a new class that inherits from `Manifest`.
   - Define the template filename and required arguments:
     ```python
     class Service(Manifest):
         template = "service.yaml.j2"
         required_args = {"name", "port"}
     ```
   - Implement any additional logic if necessary.

3. **Use the Subclass in `main.py`**
   - Import your new class in `main.py`.
   - Instantiate it with parsed arguments and call `produce_manifest()`:
     ```python
     from kubernetes import Service

     args = vars(prepare_parser())
     service = Service(args)
     manifest = service.produce_manifest()
     print(manifest)
     ```

4. **Add CLI Arguments if Needed**
   - Update `main.py` to parse any new arguments required by your resource using `argparse`.

5. **Test Your Changes**
   - Add unit tests in the `tests/` folder to validate the new resource generation.
   - Run tests with:
     ```bash
     pytest tests/
     ```
