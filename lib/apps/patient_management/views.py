
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication

from ...shared.utils import MetaResponseRenderer, StandardResultsSetPagination
from .models import *
from .serializers import *


class PatientViewset(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given patient.

    list:
    Return a list of all the existing patients.

    create:
    Create a new patient.

    update:
    Update an existing patient.

    partial_update:
    Partially update an existing patient.

    destroy:
    Delete an existing patient.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [MetaResponseRenderer]
    serializer_class = PatientSerializer

    def get_queryset(self):
        qset = Patient.objects.all()
        qset=qset.filter(user=self.request.user.pk)
        print()
        return qset

    def get_serializer(self, *args, **kwargs):
        """
        Make sure `user` fields is present otherwise append fa requesting user
        """

        if self.action in ["create","update","partial_update"] and (data := kwargs.get("data")):
            if "user" not in data:
                kwargs["data"] = {**data}
                kwargs["data"].update({"user": self.request.user.pk})

        self.kwargs["user"] = self.request.user.pk
        return super().get_serializer(*args, **kwargs)
