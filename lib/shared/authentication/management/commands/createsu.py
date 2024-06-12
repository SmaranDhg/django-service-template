import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from ...models import *

app_dir = os.path.join(settings.BASE_DIR, "apps/lalitpur")


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        email = os.environ.get("ADMIN_EMAIL", "admin@admin.com")
        password = os.environ.get("ADMIN_PASSWORD", "admin@123")

        if not User.objects.filter(email=email).exists():
            user = User.objects.get_or_create(
                email=email,
                password=make_password(password),
                is_active=True,
                is_staff=True,
                is_superuser=True,
            )[0]
            user.full_name = "Patient Mangaement System Admin"
            user.save()

        print("Complete: Superuser has been created.")
