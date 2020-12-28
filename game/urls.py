from django.urls import path

from . import views

urlpatterns = [
    # ex: /games/
    path('', views.index, name='index'),
    # ex: /games/5
    path('<int:game_id>/', views.join, name='join'),
]
