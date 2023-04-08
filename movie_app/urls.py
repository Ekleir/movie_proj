
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all_movies),
    path('movie/<slug:slug_movie>/', views.show_one_movie, name='movie-detail'),
    path('directors/', views.show_all_directors),
    path('directors/<int:direct>/', views.show_one_director, name='directors-detail')
]