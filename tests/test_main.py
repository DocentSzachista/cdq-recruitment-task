import pytest
import argparse
from main import parse_coma_values, prepare_parser


@pytest.mark.parametrize("input_str,expected", [
    ("ENV=prod,DEBUG=true", {"ENV": "prod", "DEBUG": "true"}),
    ("FOO=bar", {"FOO": "bar"}),
])
def test_parse_coma_values(input_str, expected):
    result = parse_coma_values(input_str, False)
    assert result == expected


def test_parse_coma_values_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        parse_coma_values("INVALID_STRING_WITHOUT_EQUALS", False)


def test_prepare_parser_valid(monkeypatch):
    test_args = [
        "program_name",
        "deployment",
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

@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_prepare_parser_missing_required(program, capsys, monkeypatch):
    test_args = ["program_name", program, "--image", "nginx"]  # brak --name
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit) as excinfo:
        prepare_parser()

    captured = capsys.readouterr()
    assert "the following arguments are required: --name" in captured.err
    assert excinfo.value.code == 2

@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_name_invalid(program, monkeypatch):
    test_args = ["program_name", program, "--name", "Invalid_Name!", "--image", "nginx"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        prepare_parser()


@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_name_too_long(program, monkeypatch):
    long_name = "a" * 64
    test_args = ["program_name", program, "--name", long_name, "--image", "nginx"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        prepare_parser()

@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_labels_invalid_format(program, monkeypatch):
    test_args = ["program_name", program, "--name", "app", "--image", "nginx", "--labels", "invalidlabel"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        prepare_parser()

@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_labels_invalid_value(program, monkeypatch):
    test_args = ["program_name", program, "--name", "app", "--image", "nginx", "--labels", "env=pro_"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        prepare_parser()

@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_envs_invalid_key(program, monkeypatch):
    test_args = ["program_name", program, "--name", "app", "--image", "nginx", "--envs", "9INVALID=value"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        prepare_parser()

@pytest.mark.parametrize("program", ["deployment", "pod"])
def test_envs_missing_equals(program, monkeypatch):
    test_args = ["program_name", program, "--name", "app", "--image", "nginx", "--envs", "DEBUGtrue"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        prepare_parser()
