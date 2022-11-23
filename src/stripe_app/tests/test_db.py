import pytest

from stripe_app.services.db_services import get_item, get_order


@pytest.mark.usefixtures("create_items")
@pytest.mark.django_db
def test_get_item():
    item = get_item(item_pk=pytest.item3.id)
    assert item[0]["id"] == pytest.item3.id


@pytest.mark.usefixtures("create_order_items")
@pytest.mark.django_db
def test_get_order():
    order = get_order(
        order_pk=pytest.order.id, fields=("items", "tax", "discount", "unit_amount")
    )
    assert order[0]["pk"] == pytest.order.id
    assert len(order[0]["items"]) == 2
    assert order[0]["tax"]["percentage"] == pytest.tax.percentage
    assert order[0]["discount"]["name"] == pytest.discount.name
    assert order[0]["unit_amount"] == sum(
        [
            getattr(pytest, item).price * getattr(pytest, "order_" + item).quantity
            for item in ["item1", "item2"]
        ]
    )
