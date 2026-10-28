import pytest

from campus_tracker.core import (
    Subject,
    attendance_percent,
    classes_can_skip,
    classes_needed,
    is_eligible,
    sgpa,
)


def make(name="DS", credits=4, attended=30, held=40, grade="A"):
    return Subject(name, credits, attended, held, grade)


def test_attendance_percent():
    assert attendance_percent(30, 40) == 75.0
    assert attendance_percent(0, 0) == 100.0
    assert attendance_percent(1, 3) == 33.33


@pytest.mark.parametrize("attended,held", [(30, 40), (27, 38), (0, 4), (30, 44)])
def test_classes_needed_reaches_target_minimally(attended, held):
    n = classes_needed(attended, held)
    assert attendance_percent(attended + n, held + n) >= 75
    if n > 0:
        assert attendance_percent(attended + n - 1, held + n - 1) < 75


def test_classes_needed_rejects_bad_target():
    with pytest.raises(ValueError):
        classes_needed(10, 10, target=100)


def test_classes_can_skip():
    assert classes_can_skip(30, 40) == 0
    assert classes_can_skip(38, 45) == 5
    assert attendance_percent(38, 50) >= 75
    assert attendance_percent(38, 51) < 75


def test_sgpa_is_credit_weighted():
    subjects = [make(credits=4, grade="O"), make(credits=2, grade="B")]
    assert sgpa(subjects) == round((4 * 10 + 2 * 6) / 6, 2)


def test_sgpa_requires_subjects():
    with pytest.raises(ValueError):
        sgpa([])


def test_eligibility():
    assert is_eligible(make(attended=30, held=40))
    assert not is_eligible(make(attended=29, held=40))


def test_grade_is_case_insensitive():
    assert make(grade="a+").grade_point == 9


@pytest.mark.parametrize(
    "kwargs",
    [
        {"credits": 0},
        {"attended": 41, "held": 40},
        {"attended": -1},
        {"grade": "Z"},
    ],
)
def test_subject_validation(kwargs):
    with pytest.raises(ValueError):
        make(**kwargs)
