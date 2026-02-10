from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OlympiadViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', OlympiadViewSet, basename='olympiad')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]

