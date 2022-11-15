from django.urls import path

from . import views

urlpatterns = [
    path('file', views.consume_file, name='consume_file')
]
