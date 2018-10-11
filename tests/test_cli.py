"""register_toil cli tests."""

# pylint: disable=E1135

import subprocess

from click.testing import CliRunner

from register_toil import cli


def test_register_toil(tmpdir):
    """Sample test for register_toil command."""
    runner = CliRunner()
    optdir = tmpdir.mkdir("opt")
    bindir = tmpdir.mkdir("bin")
    optexe = optdir.join("toil_disambiguate", "v0.1.2", "toil_disambiguate")
    binexe = bindir.join("toil_disambiguate_v0.1.2")
    result = runner.invoke(
        cli.register_toil,
        [
            "--pypi_name",
            "toil_disambiguate",
            "--pypi_version",
            "v0.1.2",
            "--volumes",
            "/tmp",
            "/carlos",
            "--optdir",
            optdir.strpath,
            "--bindir",
            bindir.strpath,
            "--tmpvar",
            "$TMP",
        ],
    )

    if result.exit_code:
        print(vars(result))

    for i in optexe.strpath, binexe.strpath:
        assert b"0.1.2" in subprocess.check_output(
            args=[i, "--version"], env={"TMP": "/tmp"}, stderr=subprocess.STDOUT
        )

    assert "--volumes /tmp /carlos" in optexe.read()
    assert "--workDir $TMP" in optexe.read()


def test_register_command(tmpdir):
    """Sample test for register_toil command."""
    runner = CliRunner()
    optdir = tmpdir.mkdir("opt")
    bindir = tmpdir.mkdir("bin")
    optexe = optdir.join("docker-pcapcore", "v0.1.1", "bwa_mem_pl_v0.1.1")
    binexe = bindir.join("bwa_mem_pl_v0.1.1")
    result = runner.invoke(
        cli.register_singularity,
        [
            "--image_repository",
            "docker-pcapcore",
            "--image_version",
            "v0.1.1",
            "--image_user",
            "leukgen",
            "--volumes",
            "/tmp",
            "/carlos",
            "--optdir",
            optdir.strpath,
            "--bindir",
            bindir.strpath,
            "--tmpvar",
            "$TMP",
            "--command",
            "bwa_mem.pl",
            "--target",
            "bwa_mem.pl",
        ],
    )

    if result.exit_code:
        print(vars(result))

    for i in optexe.strpath, binexe.strpath:
        assert b"4.2.1" in subprocess.check_output(
            args=[i, "--version"],
            env={"TMP": "/tmp", "USER": "root"},
            stderr=subprocess.STDOUT,
        )

    assert "--bind /tmp:/carlos" in optexe.read()
    assert "--workdir $TMP" in optexe.read()
