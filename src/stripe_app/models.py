from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ["-price"]

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(
        "Discount",
        on_delete=models.PROTECT,
        related_name="order",
        null=True,
        blank=True,
    )
    tax = models.ForeignKey(
        "Tax",
        on_delete=models.PROTECT,
        related_name="order",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order[{self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField()


class Tax(models.Model):
    class TaxTypes(models.TextChoices):
        GST = "GST", _("Goods and Services Tax")
        VAT = "VAT", _("Value-added tax")
        JCT = "JCT", _("Japanese consumption tax")
        QST = "QST", _("Québec sales tax")
        SALES = "Sales", _("Sales tax")

    tax_type = models.CharField(choices=TaxTypes.choices, max_length=50)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR
    )
    description = models.CharField(max_length=128)
    is_inclusive = models.BooleanField(default=False)

    class Meta:
        ordering = ["-percentage"]

    def __str__(self):
        return f"{str(self.tax_type).capitalize()} tax with {self.percentage}%"


class Discount(models.Model):
    class Duration(models.TextChoices):
        FOREVER = "FRVR", _("Forever")
        ONCE = "ONCE", _("Once")
        REPEAT = "RPT", _("Repeat")

    name = models.CharField(max_length=128)
    discount_value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=PERCENTAGE_VALIDATOR,
    )
    duration = models.CharField(max_length=20, choices=Duration.choices)

    class Meta:
        ordering = ["-discount_value"]

    def __str__(self):
        return f"{self.name} discount with {self.discount_value}%"
