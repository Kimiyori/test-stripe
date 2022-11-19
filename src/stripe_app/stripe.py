import stripe
from django.conf import settings
from django.urls import reverse


class StripeAPI:
    __slots__ = ("success_url", "cancel_url")
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_urls(self, request):
        domain = f"http://{request.get_host()}"
        self.success_url = f"{domain}/success"
        self.cancel_url = f"{domain}/fail"

    def create_session(self, request, items, discounts=None, tax=None):
        self.create_urls(request)
        items_list = [items] if not isinstance(items, list) else items
        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item["name"],
                        "description": item["description"],
                    },
                    "unit_amount": int(round(item["price"], 2) * 100),
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
            success_url=self.success_url,
            cancel_url=self.cancel_url,
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
