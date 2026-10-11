from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ProfileViewSet

router = DefaultRouter()

router.register(r'items', ItemViewSet, basename='item')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include(router.urls)),
]