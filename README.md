# Campus Tracker

[![CI](https://github.com/techvats07/campus-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/techvats07/campus-tracker/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A small command-line tool for college students: it reads a semester CSV,
calculates **attendance per subject** and **SGPA** on the 10-point scale, and
tells you, for each subject, how many classes you can still skip or must attend
to stay above the **75% attendance rule** for exam eligibility.

## Example

```text
$ campus-tracker data/semester.csv
Subject                  Attendance  Grade  Status
--------------------------------------------------------------------------
Data Structures              84.44%     A+  OK (can skip 5)
Operating Systems            68.18%      A  SHORT - attend next 12
Database Management          87.50%      O  OK (can skip 6)
Computer Networks            71.05%     B+  SHORT - attend next 6
Software Engineering         83.33%      A  OK (can skip 2)

SGPA: 8.44
```

## Features

- Attendance %, "classes needed" and "classes you can skip" for any target (`--target 80`)
- Credit-weighted SGPA (O, A+, A, B+, B, C, P, F grades)
- Input validation with clear error messages (missing columns, attended > held, unknown grade)
- No runtime dependencies — standard library only

## Getting started

```bash
git clone https://github.com/techvats07/campus-tracker.git
cd campus-tracker
pip install -e ".[dev]"
campus-tracker data/semester.csv
```

The CSV needs these columns:

| subject | credits | attended | held | grade |
|---|---|---|---|---|
| Data Structures | 4 | 38 | 45 | A+ |

## Continuous integration

Every push and pull request runs the [GitHub Actions workflow](.github/workflows/ci.yml):

1. **Lint** — `ruff check` and `ruff format --check`
2. **Test** — `pytest` with a 90% coverage gate on Python 3.10, 3.11, 3.12 and 3.13 (matrix build)
3. **Smoke test** — runs the CLI on the sample data

## Project structure

```text
src/campus_tracker/
├── core.py   # attendance, SGPA and eligibility logic
├── io.py     # CSV loading and validation
└── cli.py    # command-line report
tests/        # pytest suite
data/         # sample semester data
```

## License

MIT
