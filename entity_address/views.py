from django.shortcuts import render
from rest_framework.permissions import AllowAny
from .models import EntityAddressModel
from .serializers import EntityAddressSerializer
from rest_framework.viewsets import ModelViewSet


class EntityAddressViews(ModelViewSet):
    serializer_class = EntityAddressSerializer
    queryset = EntityAddressModel.objects.all()
    permission_classes = (AllowAny,)
