from django.urls import path
from .views import assistant_chat

app_name = 'assistant'
urlpatterns = [path('', assistant_chat, name='chat')]
