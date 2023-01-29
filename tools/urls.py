from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    re_path(r'^create', views.CreateToolsViews.as_view()),
    re_path(r'^get_list', views.RetrieveToolsViews.as_view())
]
