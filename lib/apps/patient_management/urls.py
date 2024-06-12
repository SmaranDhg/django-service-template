from rest_framework_nested import routers
from .views import *

base = routers.DefaultRouter()
base.register("patients", PatientViewset, basename="patients")

urlpatterns = base.urls
