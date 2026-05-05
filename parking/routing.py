from django.urls import path
from .consumers import SlotConsumer

websocket_urlpatterns = [
    path('ws/slots/', SlotConsumer.as_asgi()),
]