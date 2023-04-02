from django.db import transaction
from AndroidBackend.logger import log
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import EntityModel
from .serializers import EntitySerializer
from entity_address.models import EntityAddressModel
from entity_address.serializers import EntityAddressSerializer
from rest_framework.exceptions import NotFound, ValidationError


class EntityViews(ModelViewSet, DestroyAPIView, UpdateAPIView):
    serializer_class = EntitySerializer
    queryset = EntityModel.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication]

    # permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                log.info("In EntityViews.post")
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
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'User registered  successfully',
                }
                return Response(response, status=status.HTTP_201_CREATED)
            except ValidationError as validation_error:
                log.exception("Validation Error" + str(validation_error))
                transaction.set_rollback(True)
                return Response(dict(error=str(validation_error)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                entity_id = request.data.get("entity_id")
                address_data = request.data.pop("address")
                query_set = EntityModel.objects.get(entity_id__exact=entity_id)
                serializer = EntitySerializer(query_set, data=request.data)
                serializer.is_valid(raise_exception=True)
                # serializer.save()
                self.perform_update(serializer)

                for each_rec in address_data:
                    address_qs = EntityAddressModel.objects.get(id__exact=each_rec["id"])
                    address_serializer = EntityAddressSerializer(address_qs, data=each_rec)
                    address_serializer.is_valid(raise_exception=True)
                    address_serializer.save()
                return Response(dict(message="Entity Added/Updated", user_id=query_set.entity_id),
                                status=status.HTTP_200_OK)
            except Exception as e:
                transaction.rollback(True)
                return Response(dict(error=str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                entity_id = request.data.get("entity_id")
                try:
                    address_instance = EntityAddressModel.objects.get(entity_id__exact=entity_id)
                except:
                    address_instance = None
                if address_instance:
                    address_instance.delete()
                    # self.perform_destroy(address_instance)
                try:
                    instance = EntityModel.objects.get(entity_id__exact=entity_id)
                    self.perform_destroy(instance)
                    return Response("Success", status=status.HTTP_204_NO_CONTENT)
                except NotFound as data_not_found:
                    return Response(dict(error=str(data_not_found)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                transaction.rollback(True)
                return Response(dict(error=str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self, params):
        if params:
            return EntityModel.objects.filter(entity_id__exact=params)
        else:
            return EntityModel.objects.all().order_by("-created_on")

    def list(self, request, *args, **kwargs):
        params = request.query_params.get("entity_id")
        serializer = EntitySerializer(self.get_queryset(params), many=True)
        returned_data = []
        for each_rec in serializer.data:
            entity_id = each_rec.get("entity_id")
            address_serializer = EntityAddressModel.objects.filter(entity_id__exact=entity_id)
            ser = EntityAddressSerializer(address_serializer, many=True)
            each_rec["address"] = ser.data
            returned_data.append(each_rec)
        return Response(returned_data, status=status.HTTP_200_OK)
