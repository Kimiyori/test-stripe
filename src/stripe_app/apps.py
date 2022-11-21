# pylint: disable=missing-class-docstring, no-member
from django.apps import AppConfig
from stripe_project import container


class StripeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe_app"

    def ready(self) -> None:
        container.wire(modules=[".services.stripe_services"])
