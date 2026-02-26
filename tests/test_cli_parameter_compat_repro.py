import pytest

from android_docker.docker_cli import create_parser


def parse_args(argv):
    parser = create_parser()
    return parser.parse_args(argv)


def test_compose_subcommand_is_available():
    args = parse_args(["compose", "version"])
    assert args.subcommand == "compose"


def test_run_supports_rm_flag():
    args = parse_args(["run", "--rm", "alpine:latest", "echo", "ok"])
    assert args.rm is True


def test_rm_supports_multiple_targets():
    args = parse_args(["rm", "-f", "c1", "c2"])
    assert args.container == ["c1", "c2"]


def test_ps_supports_quiet_and_format():
    args = parse_args(["ps", "-q"])
    assert args.quiet is True
    args2 = parse_args(["ps", "--format", "{{.ID}} {{.Status}}"])
    assert args2.format == "{{.ID}} {{.Status}}"


def test_logs_supports_tail_and_since():
    args = parse_args(["logs", "--tail", "10", "--since", "1m", "c1"])
    assert args.tail == "10"
    assert args.since == "1m"


def test_images_supports_format_and_digests():
    args = parse_args(["images", "--digests"])
    assert args.digests is True
    args2 = parse_args(["images", "--format", "{{.Repository}}:{{.Tag}}"])
    assert args2.format == "{{.Repository}}:{{.Tag}}"


def test_exec_supports_env_and_user():
    args = parse_args(["exec", "-e", "A=1", "--user", "0", "c1", "env"])
    assert args.env == ["A=1"]
    assert args.user == "0"

