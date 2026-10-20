import importlib
import subprocess
import sys
from pathlib import Path

import magic

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "test" / "testdata" / "test.pdf"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "magic"] + list(args),
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )


def test_module_description():
    result = run_cli(str(PDF))
    assert result.returncode == 0
    assert result.stdout == f"{PDF}: {magic.from_file(str(PDF))}\n"
    assert result.stderr == ""


def test_module_mime():
    result = run_cli("--mime", str(PDF))
    assert result.returncode == 0
    assert result.stdout == f"{PDF}: application/pdf\n"
    assert result.stderr == ""


def test_module_continues_after_missing_file(tmp_path):
    missing = str(tmp_path / "not found.pdf")
    result = run_cli(missing, str(PDF))
    assert result.returncode == 1
    assert result.stdout == f"{PDF}: {magic.from_file(str(PDF))}\n"
    assert missing in result.stderr
    assert "Traceback" not in result.stderr


def test_module_handles_unicode_file_name(tmp_path):
    path = tmp_path / "a unicode \u00e9 file.txt"
    path.write_text("plain text\n", encoding="utf-8")
    result = run_cli(str(path))
    assert result.returncode == 0
    assert result.stdout == f"{path}: {magic.from_file(str(path))}\n"


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
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "example.pdf" in captured.err
    assert "libmagic failed" in captured.err
