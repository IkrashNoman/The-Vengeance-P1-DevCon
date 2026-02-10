from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PollViewSet,
    PollResponseViewSet,
    QnAViewSet,
)

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'responses', PollResponseViewSet, basename='poll-response')
router.register(r'qna', QnAViewSet, basename='qna')

urlpatterns = [
    path('', include(router.urls)),
]

