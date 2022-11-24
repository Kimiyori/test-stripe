import random
from typing import Any
from faker import Faker
from django.db import transaction
from django.core.management.base import BaseCommand
from stripe_app.models import Item, Order, Discount, Duration, OrderItem, Tax, TaxTypes


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        faker = Faker()
        items = []
        for _ in range(10):
            items.append(
                Item(
                    name=faker.pystr(),
                    description=faker.text(max_nb_chars=500),
                    price=faker.pyint(max_value=250),
                )
            )
        Item.objects.bulk_create(items)
        discounts = []
        taxs = []
        for _ in range(3):
            discounts.append(
                Discount(
                    name=faker.pystr(max_chars=50),
                    discount_value=faker.pyint(max_value=100),
                    duration=Duration.ONCE,
                )
            )
            taxs.append(
                Tax(
                    percentage=faker.pyint(max_value=100),
                    tax_type=TaxTypes.GST,
                    description=faker.text(max_nb_chars=128),
                )
            )
        Discount.objects.bulk_create(discounts)
        Tax.objects.bulk_create(taxs)
        orders = []
        for _ in range(2):
            orders.append(
                Order(
                    discount=discounts[random.randint(0, 2)],
                    tax=taxs[random.randint(0, 2)],
                )
            )
        Order.objects.bulk_create(orders)
        order_items = []
        for _ in range(10):
            order_items.append(
                OrderItem(
                    order=orders[random.randint(0, 1)],
                    item=items[random.randint(0, 9)],
                    quantity=faker.pyint(min_value=1, max_value=5),
                )
            )
        OrderItem.objects.bulk_create(order_items)
