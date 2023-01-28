from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.RoleViews, "role")

urlpatterns = [
    path('', include(router.urls))
]
