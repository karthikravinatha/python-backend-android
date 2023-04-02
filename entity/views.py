from django.db import transaction
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import EntityModel
from .serializers import EntitySerializer
from entity_address.models import EntityAddressModel
from entity_address.serializers import EntityAddressSerializer


class EntityViews(ModelViewSet):
    serializer_class = EntitySerializer
    queryset = EntityModel.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                serializer = EntitySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                data = serializer.save()

                address_data = request.data.get("address")
                entity_id = str(data.entity_id)
                for each_rec in address_data:
                    each_rec["entity_id"] = entity_id
                    address_serializer = EntityAddressSerializer(data=each_rec)
                    address_serializer.is_valid(raise_exception=True)
                    address_serializer.save()
                return Response("Created")
            except Exception as e:
                transaction.set_rollback(True)
                return Response(e)

    def get_queryset(self):
        return EntityModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = EntitySerializer(self.get_queryset(), many=True)
        for each_rec in serializer.data:
            entity_id = each_rec.get("entity_id")
            address_serializer = EntityAddressModel.objects.filter(entity_id__exact=entity_id)

    def list(self, request, *args, **kwargs):
        serializer = EntitySerializer(self.get_queryset(), many=True)
        returned_data = []
        for each_rec in serializer.data:
            entity_id = each_rec.get("entity_id")
            address_serializer = EntityAddressModel.objects.filter(entity_id__exact=entity_id)
            ser = EntityAddressSerializer(address_serializer, many=True)
            each_rec["address"] = ser.data
            returned_data.append(each_rec)
        return Response(returned_data)

