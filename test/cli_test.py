# Keep these tests compatible with the Python 2.7+ matrix in tox.ini.
# ruff: noqa: UP032
import importlib
import os
import subprocess
import sys
from collections import namedtuple

import magic

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "test", "testdata", "test.pdf")
CLIResult = namedtuple("CLIResult", "returncode stdout stderr")


def run_cli(*args):
    process = subprocess.Popen(
        [sys.executable, "-m", "magic"] + list(args),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout, stderr = process.communicate()
    return CLIResult(process.returncode, stdout, stderr)


def test_module_description():
    result = run_cli(PDF)
    assert result.returncode == 0
    assert result.stdout == "{}: {}\n".format(PDF, magic.from_file(PDF))
    assert result.stderr == ""


def test_module_mime():
    result = run_cli("--mime", PDF)
    assert result.returncode == 0
    assert result.stdout == "{}: application/pdf\n".format(PDF)
    assert result.stderr == ""


def test_module_continues_after_missing_file(tmpdir):
    missing = str(tmpdir.join("not found.pdf"))
    result = run_cli(missing, PDF)
    assert result.returncode == 1
    assert result.stdout == "{}: {}\n".format(PDF, magic.from_file(PDF))
    assert missing in result.stderr
    assert "Traceback" not in result.stderr


def test_module_handles_unicode_file_name(tmpdir):
    path = tmpdir.join(b"a unicode \xc3\xa9 file.txt".decode("utf-8"))
    path.write_binary(b"plain text\n")
    result = run_cli(str(path))
    assert result.returncode == 0
    assert result.stdout == "{}: {}\n".format(path, magic.from_file(str(path)))


def test_module_requires_file():
    result = run_cli()
    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert "Traceback" not in result.stderr


def test_module_reports_libmagic_failure(monkeypatch, capsys):
    cli = importlib.import_module("magic.__main__")

    def fail(filename, mime=False):
        raise magic.MagicException("libmagic failed")

    monkeypatch.setattr(cli, "from_file", fail)
    assert cli.main(["example.pdf"]) == 1
    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert "example.pdf" in stderr
    assert "libmagic failed" in stderr
