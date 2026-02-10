from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, DepartmentMemberViewSet

router = DefaultRouter()
router.register(r'', DepartmentViewSet, basename='department')
router.register(r'members', DepartmentMemberViewSet, basename='department-member')

urlpatterns = [
    path('', include(router.urls)),
]

