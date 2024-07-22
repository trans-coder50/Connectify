from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('', consumers.appOneConsumer.as_asgi()),  
    path('profile/', consumers.appOneConsumer.as_asgi()), 
    path('messages/', consumers.MessagesHandling.as_asgi()),  
    path('saves/', consumers.appOneConsumer.as_asgi()),  

]