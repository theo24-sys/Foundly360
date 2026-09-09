import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or promote a Foundry360 platform administrator from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("FOUNDRY_ADMIN_USERNAME", "").strip()
        email = os.getenv("FOUNDRY_ADMIN_EMAIL", "").strip().lower()
        password = os.getenv("FOUNDRY_ADMIN_PASSWORD", "")

        if not username or not email or not password:
            raise CommandError(
                "Set FOUNDRY_ADMIN_USERNAME, FOUNDRY_ADMIN_EMAIL, and "
                "FOUNDRY_ADMIN_PASSWORD before running this command."
            )
        if len(password) < 20:
            raise CommandError("FOUNDRY_ADMIN_PASSWORD must be at least 20 characters.")
        if username.lower() in {"admin", "administrator", "root", "user", "foundry360"}:
            raise CommandError("Choose a non-obvious administrator username.")

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} platform administrator: {user.email}"))
