"""
ASGI config for event_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')

# For now, keep ASGI simple HTTP-only. WebSocket / Channels integration
# will be added later when real-time features are implemented.
application = get_asgi_application()
