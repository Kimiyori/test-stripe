import pytest
import responses
from stripe_app.models import Discount, Duration, Item, Order, OrderItem, Tax, TaxTypes


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def create_items(faker):
    pytest.item1 = Item.objects.create(
        name=faker.pystr(),
        description=faker.text(max_nb_chars=500),
        price=faker.pyint(),
    )
    pytest.item2 = Item.objects.create(
        name=faker.pystr(),
        description=faker.text(max_nb_chars=500),
        price=faker.pyint(),
    )
    pytest.item3 = Item.objects.create(
        name=faker.pystr(),
        description=faker.text(max_nb_chars=500),
        price=faker.pyint(),
    )


@pytest.fixture
def create_discount(faker):
    pytest.discount = Discount.objects.create(
        discount_value=faker.pyint(max_value=100), duration=Duration.ONCE
    )


@pytest.fixture
def create_tax(faker):
    pytest.tax = Tax.objects.create(
        percentage=faker.pyint(max_value=100),
        tax_type=TaxTypes.GST,
        description=faker.text(max_nb_chars=128),
    )


@pytest.fixture
def create_order(create_discount, create_tax):
    pytest.order = Order.objects.create(discount=pytest.discount, tax=pytest.tax)


@pytest.fixture
def create_order_items(create_order, create_items, faker):
    pytest.order_item1 = OrderItem.objects.create(
        order=pytest.order, item=pytest.item1, quantity=faker.pyint()
    )
    pytest.order_item2 = OrderItem.objects.create(
        order=pytest.order, item=pytest.item2, quantity=faker.pyint()
    )
