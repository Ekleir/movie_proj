from django.shortcuts import render, get_object_or_404
from .models import Movie, Director, Actor
from django.db.models import F, Max, Min, Avg, Value


def show_all_movies(request):
    """Список фильмов"""

    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
        str_field=Value('hell'),
        int_bool=Value(123),
        new_budget=F('budget')+100,
        new_field=F('budget')+F('rating'),
    )
    agg = movies.aggregate(Min('rating'), Max('rating'), Avg('budget'))
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg,
    })


def show_one_movie(request, slug_movie: str):
    """Информация о фильме"""
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })


def show_all_directors(request):
    """Список режиссёров"""
    directors = Director.objects.all()
    return render(request, 'movie_app/directors.html', {'directors': directors})


def show_one_director(request, direct: int):
    """Информация о режиссере"""
    director = Director.objects.all().get(id=direct)
    return render(request, 'movie_app/one_director.html', {
        'director': director})


def show_all_actors(request):
    """Список актёров"""
    actors = Actor.objects.all()
    return render(request, 'movie_app/all_actors.html', {'actors': actors})


def show_one_actor(request, actor_id: int):
    """Информация об актёре"""
    actor = Actor.objects.all().get(id=actor_id)
    if actor.dressing:
        dressing = actor.dressing
    else:
        dressing = 'Нет информации о кабинке'
    actor_data = {
        'actor': actor,
        'dressing': dressing
    }
    return render(request, 'movie_app/one_actor.html', actor_data)
