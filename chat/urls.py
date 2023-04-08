
from . import views
from django.urls import path

from .views import *
app_name = 'chat'
urlpatterns = [
    path('chat/<str:username>', chat, name="chat"),
    path('data/<str:username>', data, name="data"),
    path('', friends, name='haus'),

]