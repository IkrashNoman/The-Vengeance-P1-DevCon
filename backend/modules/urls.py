from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet, ModuleRoundViewSet, JudgeViewSet

router = DefaultRouter()
router.register(r'', ModuleViewSet, basename='module')
router.register(r'rounds', ModuleRoundViewSet, basename='module-round')
router.register(r'judges', JudgeViewSet, basename='judge')

urlpatterns = [
    path('', include(router.urls)),
]

