from .models import EntityAddressModel
from rest_framework.serializers import ModelSerializer


class EntityAddressSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = EntityAddressModel
