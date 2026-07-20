"""
animation_utils.py

Handles SVG animation timing.
"""

ROW_DELAY = 0.075
ROW_DURATION = 0.12


def row_delay(index: int) -> float:
    """
    Delay before each row starts.

    Row 0 -> 0.00
    Row 1 -> 0.08
    Row 2 -> 0.16
    """

    return round(index * ROW_DELAY, 2)


def row_duration() -> float:
    return ROW_DURATION
