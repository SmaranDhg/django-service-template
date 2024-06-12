'''
This module contains, the shared base class and any other utitlity functionality for the serializers.
'''

from rest_framework import serializers
from .decorators import exception_handle


class _ModelSerializerMetaclass(serializers.SerializerMetaclass):
    """
    Add response type, as `__typename` field in fields.
     Default:
        `Meta.model.__name__` or `__class__.__name__`

        Override by defining
            a `_get__typename` of callable type.
        or  `__typename`  attribute in Meta class.

     Assertion: both `_get__typename()` and `Meta.__typename` cannot be set at same time.
    """

    def __new__(cls, name, bases, attrs, **kwargs):

        cls._update_attrs(name, attrs)
        cls._update_meta(attrs)
        _new_cls = super().__new__(cls, name, bases, attrs, **kwargs)

        return _new_cls

    @classmethod
    def _update_attrs(cls, name, attrs):
        _type = name
        _in_meta = False
        if Meta := attrs.get("Meta"):
            if _type := getattr(Meta, "_Meta__typename", None):
                _in_meta = True
            elif model := getattr(Meta, "model", None):
                _type = getattr(model, "__name__", name)

        _get__typename = attrs.get("_get__typename")
        if _get__typename and callable(_get__typename):
            assert _in_meta, "Cannot define `_get__typename` with `Meta.__typename`"
            attrs["__typename"] = serializers.SerializerMethodField(
                method_name="_get__typename",
                read_only=True,
                required=False,
            )
        else:
            attrs["__typename"] = serializers.CharField(
                default=_type,
                read_only=True,
                required=False,
            )

    @classmethod
    def _update_meta(cls, attrs):
        if Meta := attrs.get("Meta"):
            if (fields := getattr(Meta, "fields", "__all__")) != "__all__":
                setattr(Meta, "fields", ["__typename", *fields])


class BaseModelSerializer(
    serializers.ModelSerializer,
    metaclass=_ModelSerializerMetaclass,
):
    """
    Add response type, as `__typename` field in fields.
     Default:
        `Meta.model.__name__` or `__class__.__name__`

        Override by defining
            a `_get__typename` of callable type.
        or  `__typename`  attribute in Meta class.

     Assertion: both `_get__typename()` and `Meta.__typename` cannot be set at same time.
    """

    @property
    @exception_handle(return_on_exception="No error yet!")
    def error_message(self):
        """
        Returns `first error` of `first field`
        """
        return str(f"{list(self.errors.keys())[0]}: {list(self.errors.values())[0][0]}")


class BaseSerializer(serializers.Serializer, metaclass=_ModelSerializerMetaclass):
    """
    Add response type, as `__typename` field in fields.
     Default:
        `Meta.model.__name__` or `__class__.__name__`

        Override by defining
            a `_get__typename` of callable type.
        or  `__typename`  attribute in Meta class.

     Assertion: both `_get__typename()` and `Meta.__typename` cannot be set at same time.
    """


