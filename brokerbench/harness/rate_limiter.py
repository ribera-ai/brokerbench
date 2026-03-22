"""Rate-limiting and batching utilities for API calls.

Provides a simple token-bucket rate limiter and a batch executor
that respects rate limits when sending many requests to external
APIs (e.g., OpenRouter for LLM-judge scoring).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class RateLimiter:
    """Token-bucket rate limiter for API calls.

    Args:
        requests_per_minute: Maximum requests allowed per minute.
    """

    def __init__(self, requests_per_minute: int = 60) -> None:
        self._rpm = requests_per_minute
        self._interval = 60.0 / requests_per_minute
        self._last_call: float = 0.0

    def wait(self) -> None:
        """Block until the next call is allowed."""
        now = time.monotonic()
        elapsed = now - self._last_call
        if elapsed < self._interval:
            sleep_time = self._interval - elapsed
            logger.debug("Rate limiter sleeping %.2fs", sleep_time)
            time.sleep(sleep_time)
        self._last_call = time.monotonic()

    @property
    def requests_per_minute(self) -> int:
        """Return the configured requests-per-minute limit."""
        return self._rpm


def run_batch(
    items: list[T],
    func: Callable[[T], R],
    rate_limiter: RateLimiter | None = None,
    batch_size: int = 10,
    on_error: str = "skip",
) -> list[R | None]:
    """Execute a function over a list of items with rate limiting.

    Processes items in batches, applying rate limiting between calls.
    Useful for scoring large numbers of instances against an external
    LLM judge API.

    Args:
        items: List of items to process.
        func: Function to apply to each item.
        rate_limiter: Optional RateLimiter instance. If None, no
            rate limiting is applied.
        batch_size: Number of items per progress log message.
        on_error: Error handling strategy: "skip" (return None for
            failed items) or "raise" (re-raise the exception).

    Returns:
        List of results, with None for any skipped failures.
    """
    results: list[R | None] = []
    total = len(items)

    for i, item in enumerate(items):
        if rate_limiter is not None:
            rate_limiter.wait()

        try:
            result = func(item)
            results.append(result)
        except Exception:
            if on_error == "raise":
                raise
            logger.warning(
                "Batch item %d/%d failed, skipping",
                i + 1,
                total,
                exc_info=True,
            )
            results.append(None)

        if (i + 1) % batch_size == 0 or (i + 1) == total:
            logger.info(
                "Processed %d/%d items (%.0f%%)",
                i + 1,
                total,
                (i + 1) / total * 100,
            )

    return results
