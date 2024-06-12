"""
All the URL of the application,
setup such way, the routes are available for all the supported API version.
hence, Version Specific Response is handled from individual views.
"""

from django.contrib import admin
from django.urls import path, include
import os

from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


API_VERSIONS = ["v1"]
API_VERSION = API_VERSIONS[-1]


schema_view = get_schema_view(
    openapi.Info(
        title="Patient Assessment Management",
        default_version=API_VERSION,
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-redoc"),
]
urlpatterns += [
    path(f"api/{version}/auth/", include("lib.shared.authentication.urls"))
    for version in API_VERSIONS
]
urlpatterns += [
    path(f"api/{version}/", include("lib.apps.assessment_management.urls"))
    for version in API_VERSIONS
]
urlpatterns += [
    path(f"api/{version}/", include("lib.apps.patient_management.urls"))
    for version in API_VERSIONS
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
