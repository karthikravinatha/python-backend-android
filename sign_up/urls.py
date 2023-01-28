from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include, re_path

# router = DefaultRouter()
# router.register(r'', views.UserViews)
# router.register(r'login', views.UserLoginViews)

urlpatterns = [
    re_path(r'^signup', views.UserViews.as_view()),
    re_path(r'^signin', views.UserLoginViews.as_view())
]
