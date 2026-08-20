"""Shared quota-aware retry for LLM calls.

Google free tier has two distinct 429 modes:
  - per-minute throttle  (generate_content_free_tier_requests)  -> brief backoff, same model may recover
  - per-day quota        (GenerateRequestsPerDayPerProject...)  -> that model is DONE for the day, switch immediately

`call_with_model_rotation` tries a list of model strings, rotating on failure.
"""

from __future__ import annotations

import time
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")

_RATE_LIMIT_MARKERS = (
    "429",
    "RESOURCE_EXHAUSTED",
    # HF free tier returns these when a model is overloaded/loading — same
    # transient backoff behavior as a 429.
    "503",
    "overloaded",
    "currently loading",
    "service unavailable",
)
_DAILY_MARKERS = ("PerDay", "per_day", "requests_per_day", "requestsPerDay")
# Provider can't/won't serve this model for this request: unsupported feature
# (tool calling / structured output / json mode), gated or 404'd model, or
# unauthorized token. Not a transient error, but also not fatal for the whole
# run — skip the model and try the next one in rotation.
_UNSUPPORTED_MARKERS = (
    "not supported",
    "not implemented",
    "notimplemented",
    "does not support",
    "doesn't support",
    "unsupported",
    "tool_use_failed",
    "tool choice",
    "tool calling",
    "tool_calls",
    "function calling",
    "json mode",
    "json_validate_failed",
    "invalid_number_of_calls",
    "gated",
    "unauthorized",
    "401",
    "403",
    "404",
)


def is_rate_limit(exc: Exception) -> bool:
    return any(m in str(exc) for m in _RATE_LIMIT_MARKERS)


def is_daily_quota(exc: Exception) -> bool:
    msg = str(exc)
    return is_rate_limit(exc) and any(m in msg for m in _DAILY_MARKERS)


def is_unsupported(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(m in msg for m in _UNSUPPORTED_MARKERS)


def call_with_model_rotation(
    model_strings: Sequence[str],
    build: Callable[[str], object],
    invoke: Callable[[object], T],
    *,
    max_attempts: int = 8,
    base_backoff: float = 5.0,
    start_index: int = 0,
) -> T:
    """Try `invoke(build(m))` for each model in rotation until one succeeds.

    Per-minute 429s back off (they may recover); per-day quota means that
    model is dead until tomorrow, so jump straight to the next one.
    Unsupported-feature errors (e.g. a HuggingFace model that can't do tool
    calling or structured output) also skip straight to the next model but
    use a short delay, since they'll recur on every attempt.
    `start_index` staggers parallel branches so they don't all hit model 0
    at once.
    """
    if not model_strings:
        raise ValueError("model rotation list is empty")
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        model_str = model_strings[(start_index + attempt) % len(model_strings)]
        try:
            return invoke(build(model_str))
        except Exception as exc:  # noqa: BLE001 - we re-raise non-quota errors
            if not is_rate_limit(exc):
                if is_unsupported(exc):
                    print(
                        f"[llm] {model_str} unsupported for this task "
                        f"({type(exc).__name__}: {exc}); skipping"
                    )
                    last_exc = exc
                    time.sleep(1.0)
                    continue
                raise
            last_exc = exc
            if is_daily_quota(exc):
                # Per-day: model is spent for today. Short sleep so parallel
                # researchers don't stampede the next model simultaneously.
                delay = 2.0
            else:
                delay = min(base_backoff * (2.0 ** (attempt // max(1, len(model_strings)))), 60.0)
            print(
                f"[llm] quota 429 on {model_str} ({'daily' if is_daily_quota(exc) else 'rate'}); "
                f"retry {attempt + 1}/{max_attempts} on next model in {delay:.0f}s"
            )
            time.sleep(delay)
    raise last_exc  # type: ignore[misc]