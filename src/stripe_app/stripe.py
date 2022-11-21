import stripe
from django.conf import settings
from django.http import HttpRequest
from stripe_app.utils.app_utils import convert_to_stripe_currency, create_urls


class StripeAPI:
    """Class for connecting to stripe api"""

    stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_session(
        self,
        request: HttpRequest,
        items: list[dict[str, str | int]] | dict[str, str | int],
        discounts: list[dict[str, str]] | None = None,
        tax: stripe.TaxRate | None = None,
    ) -> stripe.checkout.Session:
        """Creatr stripe session

        Args:
            request (HttpRequest)
            items (list[dict[str, str  |  int]] | dict[str, str  |  int]): items with
            necessary data for creating items for session
            discounts (list[dict[str, str]] | None, optional): data with coupon id.
            Defaults to None.
            tax (stripe.TaxRate | None, optional): data with tax id. Defaults to None.

        Returns:
            stripe.checkout.Session
        """
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

    def create_coupon(self, data: dict[str, str | int]) -> stripe.Coupon:
        """Create stripe coupon

        Args:
            data (dict[str, str  |  int]): dict with data for creating coupon,
            must containt key 'discount_value'

        Returns:
            stripe.Coupon
        """
        return stripe.Coupon.create(percent_off=data["discount_value"])

    def create_tax(self, data: dict[str, str | int]) -> stripe.TaxRate:
        """create stripe tax

        Args:
            data (dict[str, str  |  int]): dict with data for creating tax

        Returns:
            stripe.TaxRate
        """
        return stripe.TaxRate.create(
            display_name=data["tax_type"],
            inclusive=data["is_inclusive"],
            percentage=data["percentage"],
        )

    def create_payment_intent(self, price: str | int) -> stripe.PaymentIntent:
        """Create stripe payment

        Args:
            price (str | int)

        Returns:
            stripe.PaymentIntent
        """
        intent = stripe.PaymentIntent.create(
            amount=convert_to_stripe_currency(price),
            currency="usd",
            payment_method_types=["card"],
        )
        return intent
