from django.contrib import admin
from .models import *


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "gender", "phone_number", "date_of_birth", "address")
    search_fields = ("full_name", "phone_number")
    list_filter = ("gender",)
