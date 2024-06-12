from ...shared.utils.serializers import BaseModelSerializer
from .models import *


class PatientSerializer(BaseModelSerializer):
    """
    Serializer for the Patient model.
    Inherits from BaseModelSerializer.

    Attributes:
        model: Patient - The model class that the serializer is based on.
        fields: str - Indicates that all fields of the Patient model are included in the serialization.

    """

    class Meta:
        model = Patient
        fields = "__all__"
