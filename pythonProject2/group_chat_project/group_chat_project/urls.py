#group_chat_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('accounts/', include('chat.urls')),
    path('', include('chat.urls')),
    path('', lambda request: redirect('login'), name='home'),
]
