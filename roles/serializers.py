from rest_framework import serializers
from .models import RoleModels


class RolesSerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = RoleModels
        # depth = 1
