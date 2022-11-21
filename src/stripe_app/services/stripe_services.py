from typing import Any
import stripe
from dependency_injector.wiring import Provide, inject, Closing
from django.http import HttpRequest

from stripe_project.containers import StripeContainer
from stripe_app.stripe import StripeAPI


@inject
def create_session_for_item(
    request: HttpRequest,
    item: dict[str, str | int],
    stripe_api: StripeAPI = Closing[Provide[StripeContainer.stripe_session]],
) -> stripe.checkout.Session:
    session = stripe_api.create_session(request, item)
    return session


@inject
def create_payment_for_item(
    item: dict[str, str | int],
    stripe_api: StripeAPI = Closing[Provide[StripeContainer.stripe_session]],
) -> stripe.PaymentIntent:
    session = stripe_api.create_payment_intent(item["price"])
    return session


@inject
def create_session_for_order(
    request: HttpRequest,
    order: dict[str, Any],
    stripe_api: StripeAPI = Closing[Provide[StripeContainer.stripe_session]],
) -> stripe.checkout.Session:
    discounts = None
    if not all(order["discount"][field] is None for field in order["discount"]):
        coupon = stripe_api.create_coupon(data=order["discount"])
        discounts = [{"coupon": f"{coupon.id}"}]
    tax = None
    if not all(order["tax"][field] is None for field in order["tax"]):
        tax = stripe_api.create_tax(data=order["tax"])
    session = stripe_api.create_session(
        request, order["items"], discounts=discounts, tax=tax
    )
    return session


@inject
def create_payment_for_order(
    order: dict[str, Any],
    stripe_api: StripeAPI = Closing[Provide[StripeContainer.stripe_session]],
) -> stripe.PaymentIntent:
    price = order["unit_amount"]
    if order["tax"]["percentage"]:
        price += price * (order["tax"]["percentage"] / 100)
    if order["discount"]["discount_value"]:
        price -= price * order["discount"]["discount_value"] / 100
    session = stripe_api.create_payment_intent(price)
    return session
