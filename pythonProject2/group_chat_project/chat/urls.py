# chat/urls.py
from django.urls import path
from .views import register, user_login, index, user_logout, group_chat, create_room, chat_room

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', index, name='index'),
    path('group-chat/', group_chat, name='group_chat'),
    path('create-room/', create_room, name='create_room'),
    path('chat-room/<int:room_id>/', chat_room, name='chat_room'),
]
