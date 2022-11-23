import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from stripe_app.models import Item, Order, Discount, Duration, OrderItem, Tax, TaxTypes


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        faker = Faker()
        for _ in range(10):
            Item.objects.create(
                name=faker.pystr(),
                description=faker.text(max_nb_chars=500),
                price=faker.pyint(),
            )
        for _ in range(3):
            Discount.objects.create(
                discount_value=faker.pyint(max_value=100), duration=Duration.ONCE
            )
            Tax.objects.create(
                percentage=faker.pyint(max_value=100),
                tax_type=TaxTypes.GST,
                description=faker.text(max_nb_chars=128),
            )
        for _ in range(2):
            Order.objects.create(
                discount__id=random.randint(0, 3), tax__id=random.randint(0, 3)
            )
        for _ in range(10):
            OrderItem.objects.create(
                order__id=random.randint(0, 2),
                item__id=random.randint(0, 10),
                quantity=faker.pyint(),
            )
