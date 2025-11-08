import pytest
from kubernetes import Manifest, Deployment


@pytest.fixture(params=[
    {"name": "app1", "replicas": 1, "image": "nginx:latest", "labels": None, "envs": None},
    {"name": "app2", "replicas": 3, "image": "redis:alpine", "labels": {"tier": "backend"}, "envs": None},
    {"name": "app3", "replicas": 2, "image": "python:3.11", "labels": {"tier": "frontend"}, "envs": {"ENV": "prod"}},
    {"name": "app4", "replicas": 0, "image": "busybox", "labels": {}, "envs": {}},
])
def deployment_args(request):
    return request.param


@pytest.fixture(params=[
    ({}, {"name", "image"}),
    ( {"name": "app"}, {"image"}),
    ( {"image": "nginx"}, {"name"}),
])
def required_deployment_args_sad_path(request):
    return request.param

@pytest.fixture(params=[
    ({"image": "nginx", "name": "app"}),
    ({"image": "nginx", "name": "123deploy"})
])
def required_deployment_args_happy_path(request):
    return request.param

def test_manifest_baseclass_instantiation_raises():
    with pytest.raises(TypeError):
        Manifest({})


def test_deployment_missing_required_argument_cases(required_deployment_args_sad_path):
    args, missing_args = required_deployment_args_sad_path
    with pytest.raises(ValueError) as excinfo:
        Deployment(args)
        for key in missing_args:
            assert key in str(excinfo.value)


def test_deployment_required_argument_only_provided(required_deployment_args_happy_path):
    args = required_deployment_args_happy_path
    dep = Deployment(required_deployment_args_happy_path)
    manifest = dep.produce_manifest()
    assert f"name: {args['name']}" in manifest
    assert f"image: {args['image']}" in manifest


def test_deployment_manifest_various_args_combinations(deployment_args):
    args = deployment_args
    dep = Deployment(args)
    manifest = dep.produce_manifest()

    assert f"name: {args['name']}" in manifest
    assert f"image: {args['image']}" in manifest
    assert f"replicas: {args['replicas']}" in manifest

    labels = args.get("labels")
    if labels:
        for key, value in labels.items():
            assert f"{key}: {value}" in manifest

    envs = args.get("envs")
    if envs:
        for key, value in envs.items():
            assert f"- name: {key}" in manifest
            assert f'value: "{value}"' in manifest