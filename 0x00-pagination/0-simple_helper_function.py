#!/usr/bin/env python3
"""
Helper function to calculate start and end index for pagination.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple containing the start and end indexes for a given page.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        tuple: A tuple (start_index, end_index) representing the range.
    """
    start, end = 0, 0
    for i in range(page):
        start = end
        end += page_size

    return (start, end)
