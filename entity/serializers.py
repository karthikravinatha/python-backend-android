from .models import EntityModel
from rest_framework.serializers import ModelSerializer


class EntitySerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = EntityModel
