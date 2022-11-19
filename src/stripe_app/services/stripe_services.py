from dependency_injector.wiring import Provide, inject, Closing
from django.urls import reverse
from stripe_project.containers import StripeContainer
from stripe_app.stripe import StripeAPI


@inject
def create_session_for_item(
    request, item, stripe: StripeAPI = Closing[Provide[StripeContainer.stripe_session]]
):
    session = stripe.create_session(request, item)
    return session


@inject
def create_session_for_order(
    request, order, stripe: StripeAPI = Closing[Provide[StripeContainer.stripe_session]]
):
    discounts = []
    if not all(order["discount"][field] is None for field in order["discount"]):
        coupon = stripe.create_coupon(data=order["discount"])
        discounts = [{"coupon": f"{coupon.id}"}]
    tax = stripe.create_tax(data=order["tax"])
    session = stripe.create_session(
        request, order["items"], discounts=discounts, tax=tax
    )
    return session
