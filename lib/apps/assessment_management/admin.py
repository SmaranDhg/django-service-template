from django.contrib import admin
from .models import *


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "assessment_type", "assessment_date", "final_score")
    search_fields = ("patient__full_name", "assessment_type")
    list_filter = ("assessment_type", "assessment_date")
