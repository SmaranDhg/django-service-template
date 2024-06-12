from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lib.shared.authentication'

    def ready(self) -> None:
        from lib.shared.authentication import signals