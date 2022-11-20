import stripe
from django.conf import settings

from stripe_app.utils.app_utils import convert_to_stripe_currency, create_urls


class StripeAPI:
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_session(self, request, items, discounts, tax):
        success_url, cancel_url = create_urls(request)
        items_list = [items] if not isinstance(items, list) else items
        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item["name"],
                        "description": item["description"],
                    },
                    "unit_amount": convert_to_stripe_currency(item["price"]),
                },
                "quantity": item.get("quantity", 1),
                "tax_rates": [tax["id"]] if tax else [],
            }
            for item in items_list
        ]
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            discounts=discounts if discounts else [],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session

    def create_coupon(self, data):
        return stripe.Coupon.create(percent_off=data["discount_value"])

    def create_tax(self, data):
        return stripe.TaxRate.create(
            display_name=data["tax_type"],
            inclusive=data["is_inclusive"],
            percentage=data["percentage"],
        )
    def create_payment_intent(self, price):
        intent = stripe.PaymentIntent.create(
                amount=convert_to_stripe_currency(price),
                currency='usd',
                payment_method_types=["card"],
         )
        return intent