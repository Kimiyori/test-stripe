from typing import Any
from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        username = "test_admin"
        password = "test_admin"
        email = "test_admin"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, password, email)
