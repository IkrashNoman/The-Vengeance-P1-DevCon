from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet, TeamViewSet, TeamMemberViewSet, RegistrationFormViewSet

router = DefaultRouter()
router.register(r'', RegistrationViewSet, basename='registration')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'team-members', TeamMemberViewSet, basename='team-member')
router.register(r'forms', RegistrationFormViewSet, basename='registration-form')

urlpatterns = [
    path('', include(router.urls)),
]

