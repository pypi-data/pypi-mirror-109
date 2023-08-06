"""Utilities to organize my activities."""


from datetime import datetime, timedelta
from functools import reduce

from typing import (
    Any,
    Callable,
    Iterable,
    List as _List,
)


def parse_time(time_string, day=None):
    """Transform a time string of the form HH:MM to a datetime object.

    :param time_string: A string of the form HH:MM.

    :param day:
        The day in which that time occurs, if not passed it defaults to
        ``datetime.today()``.

    :return: The datetime equivalent of the specified time.
    """
    time = datetime.strptime(time_string, "%H:%M").time()
    day = day or datetime.today()
    return datetime.combine(day, time)


def minute_dif(minuend, subtrahend):
    """Calculate the difference in minutes between two time strings.

    :param minuend: Minuend datetime.
    :param subtrahend: Subtrahend datetime.
    :return: The difference expressed in minutes.

    Example:
    >>> minute_dif('10:30', '20:45')
    615
    """
    time_a = parse_time(minuend)
    time_b = parse_time(subtrahend)
    return round((time_b - time_a).seconds / 60)


def sum_activity_values(activities, zero=0):
    """Sum all values in a tree of iterables.

    :param activities:
        a tree consisting of tuples of (<name>, <value>), where <value>
        can be an other tree

    :param zero: equivalent to zero for the type of <value>
    :return: the sum of all values
    """
    final_value = zero

    for _, value in activities:
        try:
            final_value += value

        except Exception:
            final_value += sum_activity_values(value, zero)

    return final_value


def transform_activities(activities, transform: Callable):
    """Transform activities using the ``transform`` function.

    :param activities:
        An iterable over tuples od the form (<name>, value), where value
        can be another such iterable.

    :param transform:
        A function that accepts an activity as input and returns an
        activity.

    :return: A list with the transformed activities.
    """

    def _(activity):
        try:
            return transform(activity)

        except Exception:
            return (activity[0], transform_activities(activity[1], transform))

    return [_(activity) for activity in activities]


def accommodate(boxes, sizes: Iterable[Any], zero=0):
    """Accommodate ``sizes`` on boxes with size specified by ``boxes``.

    Accommodate the elements in ``sizes`` on boxes with size specified
    by ``boxes``.

    :param boxes: An iterable with the size of each box.

    :param sizes:
        An iterable describing the size of the elements that will be
        accommodated in the boxes.

    :param zero:
        A value of the same type as the elements in ``sizes`` that
        represents the zero of this type.

    :return:
        A list of lists where each list represents a box. Boxes are in
        the same order as specified by ``boxes`` and contain the
        elements from ``sizes``.
    """
    boxes = [*boxes]
    sizes = [*sizes]
    assignments: _List[_List[Any]] = [[] for _ in range(len(boxes))]

    while sizes:
        differences = {
            b - s: (i, j) for i, b in enumerate(boxes) for j, s in enumerate(sizes)
        }

        positive_differences = [d for d in differences.keys() if d >= zero]

        min_box_index, min_size_index = differences[
            min(positive_differences)
            if positive_differences
            else max(differences.keys())
        ]

        selected_size = sizes.pop(min_size_index)
        assignments[min_box_index].append(selected_size)
        boxes[min_box_index] -= selected_size

    return assignments


def plan_my_day(  # noqa: D103
    windows: Iterable[Iterable[datetime]],
    activities,
):
    """Plan a day assigning activities to windows of time.

    :param windows:
        Iterable of pairs of datetime, representing spans of time available.

    :param activities: A mapping from activity name to activity weight.

    Example:
    >>> plan_my_day(
    ...     [
    ...         [parse_time("17:40"), parse_time("21:00")],
    ...         [parse_time("22:00"), parse_time("23:00")],
    ...     ],
    ...     {
    ... #        "wgtd": 1,
    ... #        "free_work": 1,
    ... #        "processing": 1,
    ...         "felyn": 2,
    ...         "home": 1,
    ...         "pgtd": 1,
    ...         "cuentas": 1,
    ...         "bigote": 1,
    ...         "R": 2,
    ...         "gtd": 1,
    ...     },
    ... )
    Making a plan for a total of 4:20:00.
    R: 22:00 - 22:57
    felyn: 17:40 - 18:37
    gtd: 18:37 - 19:06
    bigote: 19:06 - 19:35
    cuentas: 19:35 - 20:04
    pgtd: 20:04 - 20:33
    home: 20:33 - 21:00
    """
    window_list: _List[_List[datetime]] = [[*w] for w in windows]
    window_times = [b - a for a, b in window_list]

    total_weight = sum(activities.values())

    total_time = reduce(lambda a, b: a + b, window_times)
    print(f"Making a plan for a total of {total_time}.")

    activity_durations = {
        name: total_time * weight / total_weight for name, weight in activities.items()
    }

    while activity_durations:
        differences = {
            wt - at: (w, a)
            for w, wt in enumerate(window_times)
            for a, at in activity_durations.items()
        }

        positive_differences = [d for d in differences.keys() if d >= timedelta()]

        min_window, min_activity = differences[
            min(positive_differences)
            if positive_differences
            else max(differences.keys())
        ]

        if window_times[min_window] <= activity_durations[min_activity]:
            print(
                f"{min_activity}: "
                f'{window_list[min_window][0].strftime("%H:%M")} - '
                f'{window_list[min_window][1].strftime("%H:%M")}'
            )

            del window_list[min_window]

        else:
            nt = window_list[min_window][0] + activity_durations[min_activity]

            print(
                f"{min_activity}: "
                f'{window_list[min_window][0].strftime("%H:%M")} - '
                f'{nt.strftime("%H:%M")}'
            )

            window_list[min_window][0] = nt

        del activity_durations[min_activity]
        window_times = [b - a for a, b in window_list]
