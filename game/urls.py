from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.index, name='index'),
    path('games/new', views.new_game, name='new_game'),
    path('games/join', views.join_game, name='join_game'),
    path('games/<int:game_id>/', views.detail, name='detail'),
]
