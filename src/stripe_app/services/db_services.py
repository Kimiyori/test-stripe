from django.db.models import Sum, F, Model
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import JSONObject
from django.db.models.query import QuerySet

from stripe_app.utils.db_utils import get_objects
from stripe_app.models import Item, Order


def get_order(order_pk: int, fields: tuple[str, ...]) -> QuerySet[Model]:
    """Get order instance

    Args:
        order_pk (int): order id
        fields (tuple[str]): fields that need to include in annotate method

    Returns:
        QuerySet[dict[str | int | list[dict[str | int]]]]
    """
    annotate_fields = {
        "items": ArrayAgg(
            JSONObject(
                name=F("order_items__item__name"),
                price=F("order_items__item__price"),
                description=F("order_items__item__description"),
                currency=F("order_items__item__currency"),
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
        "unit_amount": Sum(F("order_items__item__price") * F("order_items__quantity")),
    }

    order = get_objects(
        Order.objects,  # pylint: disable=no-member
        filter={"pk": order_pk},
        annotate={field: annotate_fields[field] for field in fields},
        values=(
            "pk",
            "created_at",
        ),
    )
    return order  # type: ignore


def get_item(item_pk: int) -> QuerySet[Model]:
    """Get item instance

    Args:
        item_pk (int): item id

    Returns:
        QuerySet[dict[str,str|int]]
    """
    item = get_objects(
        Item.objects,  # pylint: disable=no-member
        filter={"pk": item_pk},
        values=("id", "name", "description", "price", "currency"),
    )
    return item  # type: ignore
