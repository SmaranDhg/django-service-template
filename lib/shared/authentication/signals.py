import json

from asgiref.sync import async_to_sync

from django.db.models.signals import *
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=User)
def create_tenent_on_create_user(sender, instance: User, created, **kwargs):
    """
    Signal receiver function that creates a tenant when a new User instance is created.

    Parameters:
        sender (class): The model class that sends the signal.
        instance (User): The User instance that triggered the signal.
        created (bool): A boolean indicating if the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    Behavior:
        - Generates a schema name based on the user's email address.
        - Limits the schema name to 63 characters.
        - Creates a new Tenant associated with the User instance.
        - Prints a message confirming the creation of the Tenant for the User.
    """
    if created:
        base_schema_name = instance.email
        schema_name = re.sub(r"\W|^(?=\d)", "_", base_schema_name.lower())
        schema_name = schema_name[:63]
        Tenant.of_user(instance, new_on_absent=True)

        print(f"INFO: Tenant Created for User: {instance}")
