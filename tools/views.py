from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .serializers import ToolsSerializers
from .models import ToolsModel
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status


# Create your views here.
class CreateToolsViews(generics.CreateAPIView):
    serializer_class = ToolsSerializers
    queryset = ToolsModel.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classe = JSONWebTokenAuthentication

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status_code': status.HTTP_201_CREATED,
            'message': 'Tools Created Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


class RetrieveToolsViews(generics.ListCreateAPIView):
    serializer_class = ToolsSerializers
    queryset = ToolsModel.objects.all()
    permission_classes = [AllowAny, ]

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        tool_id = request.GET.get("tool_id", None)
        if tool_id:
            serializer = ToolsSerializers(query_set.filter(tool_id=tool_id), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = ToolsSerializers(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
