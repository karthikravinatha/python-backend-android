from rest_framework import serializers
from .models import ToolsModel


class ToolsSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('tool_id', 'tool_name', 'display_name', 'description')
        model = ToolsModel
