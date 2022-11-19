from stripe_app.utils.db_utils import get_objects
from stripe_app.models import Order
from django.db.models import Sum, F
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import JSONObject


def get_order(pk):
    order = get_objects(
        Order.objects,
        filter={"pk": pk},
        annotate={
            "items": ArrayAgg(
                JSONObject(
                    name=F("order_items__item__name"),
                    price=F("order_items__item__price"),
                    description=F("order_items__item__description"),
                    quantity=F("order_items__quantity"),
                ),
            ),
            "discount": JSONObject(
                name=F("discount__name"),
                discount_value=F("discount__discount_value"),
            ),
            "tax": JSONObject(
                tax_type=F("tax__tax_type"),
                percentage=F("tax__percentage"),
                is_inclusive=F("tax__is_inclusive"),
            ),
            "unit_amount": Sum(
                F("order_items__item__price") * F("order_items__quantity")
            ),
        },
        values=(
            "pk",
            "created_at",
        ),
    )
    return order
