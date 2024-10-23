from django.contrib import admin
from django.urls import include, path
from django.views.generic import *
import app.views as views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.IndexView.as_view(), name='index'),
    path('conversao/', views.ConversaoView.as_view(), name='conversao'),
    path('conversaoPLA/', views.ConversaoPLAView.as_view(), name='PLA'),
    path('conversaoVID/', views.ConversaoVIDView.as_view(), name='VID'),
    path('conversaoIMG/', views.ConversaoIMGView.as_view(), name='IMG'),
    path('historico/', views.HistoricoView.as_view(), name='historico'),
]