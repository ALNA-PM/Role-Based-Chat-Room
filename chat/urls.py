from django.urls import path
from .views import chat_view, mentionable_users

urlpatterns = [
    path('chat/', chat_view, name='chat'),
    path('mentionable-users/', mentionable_users, name='mentionable_users'),
]

