import pytest
from main import parse_coma_values, prepare_parser
from kubernetes import Deployment

@pytest.mark.parametrize("input_str,expected", [
    ("ENV=prod,DEBUG=true", {"ENV": "prod", "DEBUG": "true"}),
    ("FOO=bar", {"FOO": "bar"}),
])
def test_parse_coma_values(input_str, expected):
    result = parse_coma_values(input_str)
    assert result == expected


def test_parse_coma_values_invalid():
    with pytest.raises(ValueError):
        parse_coma_values("INVALID_STRING_WITHOUT_EQUALS")


def test_prepare_parser(monkeypatch):
    test_args = [
        "program_name",
        "--name", "myapp",
        "--image", "nginx",
        "--replicas", "2",
        "--labels", "tier=backend,env=prod",
        "--envs", "ENV=prod,DEBUG=true"
    ]
    monkeypatch.setattr("sys.argv", test_args)
    args = prepare_parser()

    assert args.name == "myapp"
    assert args.image == "nginx"
    assert args.replicas == 2
    assert args.labels == {"tier": "backend", "env": "prod"}
    assert args.envs == {"ENV": "prod", "DEBUG": "true"}


def test_deployment_integration(monkeypatch):
    test_args = [
        "program_name",
        "--name", "app1",
        "--image", "nginx",
        "--replicas", "1",
        "--labels", "tier=backend",
        "--envs", "ENV=prod"
    ]
    monkeypatch.setattr("sys.argv", test_args)
    args = vars(prepare_parser())

    dep = Deployment(args)
    manifest = dep.produce_manifest()

    assert "app1" in manifest
    assert "nginx" in manifest
    assert "replicas: 1" in manifest
    assert "tier: backend" in manifest
    assert '- name: ENV' in manifest and 'value: "prod"' in manifest


def test_parser_missing_required(capsys, monkeypatch):
    test_args = ["program_name", "--image", "nginx"]  # missing --name
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit) as excinfo:  # argparse exits with 2
        prepare_parser()

    captured = capsys.readouterr()
    assert "the following arguments are required: --name" in captured.err
    # exit code 2
    assert excinfo.value.code == 2
