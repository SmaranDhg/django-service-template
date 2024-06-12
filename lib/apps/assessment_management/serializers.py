

from lib.apps.patient_management.models import Patient
from ...shared.utils.serializers import BaseModelSerializer
from ...shared.authentication.models import User
from rest_framework import serializers
from .models import *


class AssessmentSerializer(BaseModelSerializer):

    def validate_patient(self, patient: Patient):
        """
        Validate the patient associated with the assessment.

        Parameters:
        - patient (Patient): The patient object to be validated.

        Returns:
        - Patient: The validated patient object.

        Raises:
        - serializers.ValidationError: If the patient does not belong to the user making the request.
        """
        user: User = self.context.get("request").user


        if not Patient.of_user(user, return_all=True).filter(pk=patient.pk).exists():
            raise serializers.ValidationError(f"Cannot find patient for the user!")

        return patient

    class Meta:
        model = Assessment
        fields = "__all__"
