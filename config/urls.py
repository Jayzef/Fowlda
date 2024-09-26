from django.contrib import admin
from django.urls import include, path
from django.views.generic import *
import app.views as views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.IndexView.as_view(), name='index'),
    path('conversao/', views.ConversaoView.as_view(), name='conversao'),
]
