"""Load subjects from a CSV file."""

from __future__ import annotations

import csv
from pathlib import Path

from .core import Subject

REQUIRED_COLUMNS = {"subject", "credits", "attended", "held", "grade"}


def load_subjects(path: str | Path) -> list[Subject]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")
        return [
            Subject(
                name=row["subject"].strip(),
                credits=int(row["credits"]),
                attended=int(row["attended"]),
                held=int(row["held"]),
                grade=row["grade"].strip(),
            )
            for row in reader
        ]
