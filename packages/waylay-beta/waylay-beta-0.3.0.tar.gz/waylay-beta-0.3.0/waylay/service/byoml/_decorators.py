"""Resource action method decorators specific for the 'byoml' service."""

from functools import wraps
from tenacity import (
    Retrying,
    before_sleep,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential,
    before_sleep_log,
    retry_if_exception
)
import logging

from simple_rest_client.exceptions import ErrorWithResponse

from ._exceptions import (
    ByomlActionError
)

logger = logging.getLogger(__name__)

TEMPORARY_FAILURES = [
    409,
    429,
    500,
    502,
    503,
    504,
    508
]
WAIT_EXPONENTIAL = {
    "multiplier": 1,
    "min": 4,
    "max": 32
}
DEFAULT_RETRY_ATTEMPTS = 20
DEFAULT_RETRY_MAX_DELAY = 120


def byoml_exception_decorator(action_method):
    """Create a decorator that parses json error responses."""
    @wraps(action_method)
    def wrapped(*args, **kwargs):
        try:
            return action_method(*args, **kwargs)
        except ErrorWithResponse as exc:
            raise ByomlActionError.from_cause(exc) from exc
    return wrapped


def byoml_retry_decorator(action_method):
    """Create a decorator that retries after certain exceptions."""
    @wraps(action_method)
    def wrapped(*args, **kwargs):
        retry_attempts = kwargs.pop('retry_attempts', DEFAULT_RETRY_ATTEMPTS)
        retry_max_delay = kwargs.pop('retry_max_delay', DEFAULT_RETRY_MAX_DELAY)
        for attempt in Retrying(
            stop=(stop_after_attempt(retry_attempts) | stop_after_delay(retry_max_delay)),
            retry=retry_if_exception(is_temporary_failure),
            before_sleep=before_sleep_log(logger, logging.INFO),
            wait=wait_exponential(**WAIT_EXPONENTIAL),
            reraise=True
        ):
            with attempt:
                return action_method(*args, **kwargs)
    retry_attempts_arg = f'retry_attempts={DEFAULT_RETRY_ATTEMPTS}'
    retry_max_delay_arg = f'retry_max_delay={DEFAULT_RETRY_MAX_DELAY}'
    wrapped.__doc__ = ((wrapped.__doc__ or '') + f"""
Retries on temporary failures (HTTP status codes {', '.join(str(c) for c in TEMPORARY_FAILURES)}).
Arguments that configure retry:
    {retry_attempts_arg:30}: Maximal number of retries.
    {retry_max_delay_arg:30}: Maximal delay in seconds.
""")
    return wrapped


def is_temporary_failure(exc):
    """Check if given exception is temporary."""
    return hasattr(exc, "response") and exc.response.status_code in TEMPORARY_FAILURES
