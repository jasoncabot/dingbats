from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.index, name='index'),
    path('games/<int:game_id>/', views.detail, name='detail'),
]
