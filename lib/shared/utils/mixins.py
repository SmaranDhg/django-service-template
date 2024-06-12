from typing import TypeVar
from django.db import models


_T = TypeVar("_T", bound="ModelMixin")


class ModelMixin(models.Model):

    @classmethod
    def attrs(self) -> "set":
        return {
            attr
            for attr in vars(self)
            if not callable(getattr(self, attr)) and not attr.startswith("_")
        }

    class Meta:
        abstract = True


class DateTimeMixin(ModelMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
