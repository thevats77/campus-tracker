"""Core calculations: attendance, SGPA and exam eligibility."""

from __future__ import annotations

from dataclasses import dataclass

# 10-point grading scale used by most Indian universities.
GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "P": 4,
    "F": 0,
}

MIN_ATTENDANCE = 75.0


@dataclass(frozen=True)
class Subject:
    name: str
    credits: int
    attended: int
    held: int
    grade: str

    def __post_init__(self) -> None:
        if self.credits <= 0:
            raise ValueError(f"{self.name}: credits must be positive")
        if self.held < 0 or self.attended < 0:
            raise ValueError(f"{self.name}: class counts cannot be negative")
        if self.attended > self.held:
            raise ValueError(f"{self.name}: attended ({self.attended}) > held ({self.held})")
        if self.grade.upper() not in GRADE_POINTS:
            raise ValueError(f"{self.name}: unknown grade '{self.grade}'")

    @property
    def attendance(self) -> float:
        return attendance_percent(self.attended, self.held)

    @property
    def grade_point(self) -> int:
        return GRADE_POINTS[self.grade.upper()]


def attendance_percent(attended: int, held: int) -> float:
    """Attendance as a percentage, rounded to 2 decimals. No classes held -> 100%."""
    if held == 0:
        return 100.0
    return round(attended / held * 100, 2)


def classes_needed(attended: int, held: int, target: float = MIN_ATTENDANCE) -> int:
    """Consecutive classes a student must attend to reach `target` percent."""
    if not 0 < target < 100:
        raise ValueError("target must be between 0 and 100 (exclusive)")
    needed = 0
    while attendance_percent(attended + needed, held + needed) < target:
        needed += 1
    return needed


def classes_can_skip(attended: int, held: int, target: float = MIN_ATTENDANCE) -> int:
    """Classes a student can miss in a row and still stay at or above `target`."""
    skip = 0
    while attendance_percent(attended, held + skip + 1) >= target:
        skip += 1
    return skip


def sgpa(subjects: list[Subject]) -> float:
    """Credit-weighted grade point average for a semester."""
    if not subjects:
        raise ValueError("at least one subject is required")
    total_credits = sum(s.credits for s in subjects)
    weighted = sum(s.credits * s.grade_point for s in subjects)
    return round(weighted / total_credits, 2)


def is_eligible(subject: Subject, target: float = MIN_ATTENDANCE) -> bool:
    return subject.attendance >= target
