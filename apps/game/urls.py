from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage,name = 'homePage'),
    #path('game-over',views.game_over, name="game_over")
]