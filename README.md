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
