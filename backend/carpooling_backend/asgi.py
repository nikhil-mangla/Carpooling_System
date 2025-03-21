import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carpooling_backend.settings')


django_asgi_app = get_asgi_application()


from rides.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})