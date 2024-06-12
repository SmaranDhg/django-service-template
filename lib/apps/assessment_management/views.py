# Django imports
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication

from ...shared.utils import MetaResponseRenderer, StandardResultsSetPagination
from .models import Assessment
from .serializers import AssessmentSerializer


class AssessmentViewset(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [MetaResponseRenderer]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["assessment_type", "assessment_date", "patient"]
    ordering_fields = ["assessment_date", "final_score"]
    search_fields = ["patient__full_name"]

    def get_queryset(self):
        qset = Assessment.objects.filter(patient__user_id=self.request.user.pk)
        return qset
