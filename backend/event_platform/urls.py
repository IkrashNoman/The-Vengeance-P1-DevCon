"""
URL configuration for event_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    """Health check endpoint for backend monitoring"""
    return Response({
        "status": "ok",
        "message": "Backend API is running",
        "version": "1.0"
    })

urlpatterns = [
    path('', health_check, name='health_check'),
    path('api/', health_check, name='api_health_check'),
    path('admin/', admin.site.urls),

    path('api/auth/', include('accounts.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/olympiad/', include('olympiad_core.urls')),
    path('api/modules/', include('modules.urls')),
    path('api/sports/', include('sports.urls')),
    path('api/societies/', include('societies.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/events/', include('events.urls')),
    path('api/registrations/', include('registrations.urls')),
    path('api/venues/', include('venues.urls')),
    path('api/networking/', include('networking.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/interactions/', include('interactions.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/analytics/', include('analytics.urls')),
    # Admin dashboard API
    path('api/admin/', include('admin_api.urls')),
]
