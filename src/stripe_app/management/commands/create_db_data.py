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
                Item.objects.create(
                    name=faker.pystr(),
                    description=faker.text(max_nb_chars=500),
                    price=faker.pyint(),
                )
            )
        discounts = []
        taxs = []
        for _ in range(3):
            discounts.append(
                Discount.objects.create(
                    discount_value=faker.pyint(max_value=100), duration=Duration.ONCE
                )
            )
            taxs.append(
                Tax.objects.create(
                    percentage=faker.pyint(max_value=100),
                    tax_type=TaxTypes.GST,
                    description=faker.text(max_nb_chars=128),
                )
            )
        orders = []
        for _ in range(2):
            orders.append(
                Order.objects.create(
                    discount=discounts[random.randint(0, 2)],
                    tax=taxs[random.randint(0, 2)],
                )
            )
        for _ in range(10):
            OrderItem.objects.create(
                order=orders[random.randint(0, 1)],
                item=items[random.randint(0, 9)],
                quantity=faker.pyint(),
            )
