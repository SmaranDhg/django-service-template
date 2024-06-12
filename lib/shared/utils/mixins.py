from django.db import models


class ModelMixin(models.Model):
    """
    Abstract base class for model mixins.

    Attributes:
        attrs (classmethod): A method that returns a set of attributes of the class that are not callable and do not start with an underscore.

    Meta:
        abstract (bool): Indicates that this class is abstract and should not be instantiated directly.
    """

    @classmethod
    def attrs(self) -> "set":
        return {
            attr
            for attr in vars(self)
            if not callable(getattr(self, attr)) and not attr.startswith("_")
        }

    class Meta:
        abstract = True
