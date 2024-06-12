from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import *

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="user-login",
    ),
    path("refresh/", TokenRefreshView.as_view()),
    path("register/", UserRegistrationAPI.as_view()),

]
