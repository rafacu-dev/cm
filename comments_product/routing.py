from django.urls import re_path,path

from .consumers import SignallingConsumer,ChatConsumer


"""from configobj import ConfigObj
conf = ConfigObj(profile.CONFIG_INI_URL,encoding="utf-8")"""

websocket_urlpatterns = [
    #path(conf["intranet"]["address"].split("/")[3]+"/", SignallingConsumer.as_asgi())
    #re_path(r'ws/comments/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    path('ws/comments/<str:room_name>/', ChatConsumer.as_asgi()),
]