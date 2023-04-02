from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer, UserLoginSerializer, UserListSerializer
from .models import UserModel


# Create your views here.
class UserViews(CreateAPIView, RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    # queryset = UserModel.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'User registered  successfully',
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def get_queryset(self):
        return UserModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # instance = UserModel.objects.all().values()
        serialiser = UserListSerializer(self.get_queryset(), many=True)
        return Response(serialiser.data)


class UserLoginViews(RetrieveAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = UserLoginSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_instance: UserModel = UserModel.objects.get(email_id=request.data['email'])
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
            'user_id': user_instance.user_id
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
