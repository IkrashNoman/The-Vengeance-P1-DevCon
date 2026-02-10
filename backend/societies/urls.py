from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocietyViewSet, SocietyMemberViewSet

router = DefaultRouter()
router.register(r'', SocietyViewSet, basename='society')
router.register(r'members', SocietyMemberViewSet, basename='society-member')

urlpatterns = [
    path('', include(router.urls)),
]

