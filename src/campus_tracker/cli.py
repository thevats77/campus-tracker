"""Command-line report: `campus-tracker data/semester.csv`."""

from __future__ import annotations

import argparse
import sys

from .core import MIN_ATTENDANCE, Subject, classes_can_skip, classes_needed, is_eligible, sgpa
from .io import load_subjects


def build_report(subjects: list[Subject], target: float = MIN_ATTENDANCE) -> str:
    header = f"{'Subject':<24}{'Attendance':>11}{'Grade':>7}  Status"
    lines = [header, "-" * (len(header) + 22)]
    for s in subjects:
        if is_eligible(s, target):
            status = f"OK (can skip {classes_can_skip(s.attended, s.held, target)})"
        else:
            status = f"SHORT - attend next {classes_needed(s.attended, s.held, target)}"
        lines.append(f"{s.name:<24}{s.attendance:>10.2f}%{s.grade:>7}  {status}")
    lines.append("")
    lines.append(f"SGPA: {sgpa(subjects):.2f}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Attendance and SGPA report for a semester.")
    parser.add_argument("csv", help="CSV with columns: subject,credits,attended,held,grade")
    parser.add_argument(
        "--target", type=float, default=MIN_ATTENDANCE, help="minimum attendance %% (default 75)"
    )
    args = parser.parse_args(argv)

    try:
        subjects = load_subjects(args.csv)
        print(build_report(subjects, args.target))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
