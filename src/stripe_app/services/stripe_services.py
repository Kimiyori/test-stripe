from dependency_injector.wiring import Provide, inject, Closing
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
    discounts = None
    if not all(order["discount"][field] is None for field in order["discount"]):
        coupon = stripe.create_coupon(data=order["discount"])
        discounts = [{"coupon": f"{coupon.id}"}]
    tax=None
    if not all(order["tax"][field] is None for field in order["tax"]):
        tax = stripe.create_tax(data=order["tax"])
    session = stripe.create_session(
        request, order["items"], discounts=discounts, tax=tax
    )
    return session

@inject
def create_payment_for_item(
    request, item, stripe: StripeAPI = Closing[Provide[StripeContainer.stripe_session]]
):
    session = stripe.create_payment_intent(item.price
    )
    return session

@inject
def create_payment_for_order(
    request, order, stripe: StripeAPI = Closing[Provide[StripeContainer.stripe_session]]
):  
    price=order['unit_amount']
    if order['tax']["percentage"]:
        price+=price*(order['tax']["percentage"]/100)
    if order['discount']['discount_value']:
        price-=price*order['discount']['discount_value']/100
    session = stripe.create_payment_intent(price
    )
    return session
