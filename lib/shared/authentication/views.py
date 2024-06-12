# Django imports
from pprint import pprint

from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets
from rest_framework.decorators import action

# Django Rest Framework Imports
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication

from ...shared.utils import MetaResponseRenderer, StandardResultsSetPagination
from .models import *
from .serializers import *
from rest_framework.response import Response

# Extra modules

from django.contrib.auth.hashers import make_password


class UserRegistrationAPI(GenericAPIView):

    permission_classes = []
    serializer_class = UserRegistrationSerializer
    renderer_classes = [MetaResponseRenderer]

    def post(self, request, *args, **kwargs):
        email = self.request.data.get("email")
        password = self.request.data.get("password")
        UserRegistrationSerializer(data=request.data).is_valid(raise_exception=True)

        if User.objects.filter(email=email).exists():
            return Response(
                "Please try with different email address", status=HTTP_401_UNAUTHORIZED
            )

        User.objects.create(
            email=email,
            password=make_password(password),
        )

        return Response("Resgistration successfull!", status=HTTP_201_CREATED)
