from django.urls import path
from .views import open_room, create_room, status_update, admin, rooms_api, MessageList

urlpatterns = [
    path('messenger/<str:uuid>', open_room, name='open_room'),
    path('api/createroom/<str:uuid>/', create_room),
    path('api/statusupdate/', status_update),
    path('api/rooms/', rooms_api),
    path('api/getmsg/<str:uuid>', MessageList.as_view()),
    path('chat-admin', admin, name='admin'),
]