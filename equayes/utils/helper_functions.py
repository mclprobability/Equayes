#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provides functions which are useful troughout the package."""

import time
from functools import wraps


def timeit(func):
    """
    Decorator to time function's execution time

    Args:
        func (Callable): any function to time

    Returns:
        dynamic: returns the value also func returns
    """

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
