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
| `program`     | Yes      | -       | Resource type to generate. Possible options: deployment, pod
| `--name`    | Yes      | –       | Name of the deployment and container. Must follow DNS-1123 naming rules. |
| `--image`   | Yes      | –       | Docker image to use for the container. |
| `--replicas`| No       | 3       | Number of pod replicas the deployment will create. |
| `--labels`  | No       | –       | Comma-separated key=value pairs to label the deployment. |
| `--envs`    | No       | –       | Comma-separated environment variables for the container in VAR=value format. |

## Example usage

```bash
python main.py \
  deployment \
  --name nginx \
  --image nginx \
  --replicas 2 \
  --labels app=myapp,env=dev \
  --envs DEBUG=True,LOG_LEVEL=info
```

It creates a Deployment manifest and prints it on the screen

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: myapp
    env: dev
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      env: dev
  template:
    metadata:
      labels:
        app: myapp
        env: dev
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          env:
          - name:  DEBUG
            value: "True"
          - name: LOG_LEVEL
            value: "info"
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
     command = args.pop("command")
     if command == "deployment":
         resource = Deployment(args)
     if command == "pod":
         resource = Pod(args)
     if command == "service":
         resource = Service(args)
     print(resource.produce_manifest())
     ```

4. **Add CLI Arguments if Needed**
   - Update `main.py` to parse any new arguments required by your resource using `argparse`.

5. **Test Your Changes**
   - Add unit tests in the `tests/` folder to validate the new resource generation.
   - Run tests with:
     ```bash
     pytest tests/
     ```

## Github Action feature
Here is short documentation how it would work outside of github repo if I had added it to the Github marketplace. Currently it works only on this repo by using following call:
```yaml
        - name: Generate Kubernetes deployment
          uses: ./
          with:
            ## args
```
Sample usage is stored here [link](https://github.com/DocentSzachista/cdq-recruitment-task/blob/master/.github/workflows/generate_deployment.yaml)

### ⚙️ Inputs

| Name | Description | Required | Default |
|------|--------------|-----------|----------|
| **`name`** | Object and container name in the Deployment manifest. | ✅ Yes | — |
| **`labels`** | Labels in `<key>=<value>` format, comma-separated. If not provided, the `metadata.labels` field will not be created. | ❌ No | — |
| **`replicas`** | Number of replicas (`spec.replicas`) indicating how many pods should be created. | ❌ No | `3` |
| **`envs`** | List of environment variables in `<NAME>=<value>` format, comma-separated. | ❌ No | — |
| **`filename`** | Path to the output file. If the `.yaml` extension is missing, it will be automatically added. | ✅ Yes | — |


## 🚀 Example usage

```yaml
name: Generate Kubernetes Deployment

on:
  workflow_dispatch:
    inputs:
      name:
        description: "Application name"
        required: true
        default: "my-app"

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate Deployment manifest
        uses: docent-szachista/kubernetes-manifest-generator@v1
        with:
          name: my-app
          labels: app=my-app,env=prod
          replicas: 4
          envs: DEBUG=true,LOG_LEVEL=info
          filename: k8s/deployment.yaml
```
### How it works

1. Installs Python 3.10

2. Installs dependencies from requirements.txt

3. Builds runtime parameters based on the provided inputs

4. Runs the generator using:
`python main.py deployment [options]`
5. Saves file to `k8s/deployment.yaml` file