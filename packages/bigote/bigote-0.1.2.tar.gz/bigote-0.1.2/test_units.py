"""Tests for bigote module."""


from datetime import timedelta


from bigote import accommodate, sum_activity_values


def test_smoke_accommodate():
    """Smoke test for the accommodate function."""
    assert accommodate([9, 5], [1, 2, 3, 6]) == [[6, 1], [3, 2]]


def test_accommodate_with_times():
    """Test that accommodate works well with times."""
    windows = [timedelta(seconds=9 * 60 * 60), timedelta(seconds=5 * 60 * 60)]

    activities = [
        timedelta(seconds=1 * 60 * 60),
        timedelta(seconds=2 * 60 * 60),
        timedelta(seconds=3 * 60 * 60),
        timedelta(seconds=6 * 60 * 60),
    ]

    assert accommodate(windows, activities, zero=timedelta()) == [
        [timedelta(seconds=6 * 60 * 60), timedelta(seconds=1 * 60 * 60)],
        [timedelta(seconds=3 * 60 * 60), timedelta(seconds=2 * 60 * 60)],
    ]


def test_smoke_sum_activity_values():
    """Smoke test for sum_activity_values_function."""
    result = sum_activity_values(
        [
            ("a", 3),
            ("b", 4),
            (
                "cd",
                [
                    ("c", 3),
                    ("d", 4),
                ],
            ),
        ]
    )

    assert result == 14
