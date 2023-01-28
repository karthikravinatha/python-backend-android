from django.shortcuts import render
from rest_framework import viewsets
from .models import RoleModels
from .serializers import RolesSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.


class RoleViews(viewsets.ModelViewSet):
    serializer_class = RolesSerializers
    queryset = RoleModels.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = [JSONWebTokenAuthentication]
    # authentication_class = JSONWebTokenAuthentication
    # permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication
