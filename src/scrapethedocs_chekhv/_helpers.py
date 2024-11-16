"""
Private helper functions for the scrapethedocs module
"""

import asyncio
from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def _to_sync(func: Callable[P, Awaitable[T]]) -> Callable[P, T]:  # pragma: no cover
    """
    Wraps an async function to convert it to a synchronous function

    Args:
        func:   an async function

    Returns:
        func:   a synchronous function

    """

    @wraps(func)
    def run(*args: P.args, **kwargs: P.kwargs):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            raise RuntimeError(f"Use {func.__name__} when calling inside an asyncio event loop.")

        return loop.run_until_complete(func(*args, **kwargs))

    return run
