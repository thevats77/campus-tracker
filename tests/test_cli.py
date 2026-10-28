from pathlib import Path

from campus_tracker.cli import main

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "semester.csv"


def test_report_on_sample_data(capsys):
    assert main([str(SAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "SGPA:" in out
    assert "Operating Systems" in out
    assert "SHORT - attend next" in out


def test_missing_columns(tmp_path, capsys):
    bad = tmp_path / "bad.csv"
    bad.write_text("subject,credits\nDS,4\n", encoding="utf-8")
    assert main([str(bad)]) == 1
    assert "missing columns" in capsys.readouterr().err


def test_missing_file(capsys):
    assert main(["does-not-exist.csv"]) == 1
    assert "error:" in capsys.readouterr().err
