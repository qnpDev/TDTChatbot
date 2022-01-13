from django.urls import path
from . import views
from . import worker

urlpatterns = [
   # path('', views.index)
   path('', worker.ApiChatbot.as_view(), name='chatbot')
]