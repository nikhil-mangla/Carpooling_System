import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from rides.routing import websocket_urlpatterns  # Explicitly import from rides.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carpooling_backend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),  # Fixed reference to websocket_urlpatterns
})