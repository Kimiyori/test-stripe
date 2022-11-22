from typing import Any, Callable, TypeVar
from functools import wraps
from django.http import HttpRequest, HttpResponseServerError
import stripe

StripeT = TypeVar("StripeT")


def convert_to_stripe_currency(amount: int | str) -> int:
    return int(round(int(amount), 2) * 100)


def create_urls(request: HttpRequest) -> tuple[str, str]:
    domain = f"http://{request.get_host()}"
    success_url = f"{domain}/success"
    cancel_url = f"{domain}/fail"
    return success_url, cancel_url


def stripe_error_handler(func: Callable[..., StripeT]) -> Callable[..., StripeT]:
    @wraps(func)
    def stripe_wrapper(*args: Any, **kwargs: Any) -> StripeT:
        try:
            return func(*args, **kwargs)
        except stripe.error.StripeError as error:
            raise HttpResponseServerError(  # type:ignore  # pylint: disable=raising-non-exception
                "something went wrong"
            ) from error

    return stripe_wrapper
