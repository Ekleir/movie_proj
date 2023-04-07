from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.db.models import F, Sum, Max, Min, Avg, Count, Value


# Create your views here.


def show_all_movies(request):
    # movies = Movie.objects.order_by(F('year').desc(nulls_last=True), 'rating')
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
        str_field=Value('hell'),
        int_field=Value(123),
        new_budget=F('budget')+100,
        new_field=F('budget')+F('rating'),
    )
    agg = movies.aggregate(Min('rating'), Max('rating'), Avg('budget'))
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg,
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })