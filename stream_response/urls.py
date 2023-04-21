from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("stream_message/", views.stream_message)
]
