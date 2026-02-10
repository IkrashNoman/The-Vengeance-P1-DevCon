from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthenticationView, UserViewSet, UserPermissionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'permissions', UserPermissionViewSet, basename='permission')

urlpatterns = [
    # Authentication endpoints
    path('login/', AuthenticationView.as_view(), {'action': 'login'}, name='login'),
    path('signup/', AuthenticationView.as_view(), {'action': 'signup'}, name='signup'),
    
    # Router URLs
    path('', include(router.urls)),
]
