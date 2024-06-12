from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *

base = routers.DefaultRouter()
base.register("assessments", AssessmentViewset, basename="patients")

urlpatterns = base.urls
