import os
import django
from django.db import connection
from django.db.models import Q, Count, Avg, F, Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions

from datetime import date
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    q_name = Q(full_name__icontains=search_name)
    q_nationality = Q(nationality__icontains=search_nationality)
    if search_name is not None and search_nationality is not None:
        query = Q(q_name) & Q(q_nationality)
    elif search_nationality is not None:
        query = Q(q_nationality)
    else:
        query = Q(q_name)

    directors = Director.objects.filter(query).order_by('full_name')
    if not directors:
        return ''

    return '\n'.join(f"Director: "
                     f"{d.full_name}, "
                     f"nationality: {d.nationality}, "
                     f"experience: {d.years_of_experience}"
                     for d in directors)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return (f"Top Director: "
            f"{top_director.full_name}, "
            f"movies: {top_director.number_of_movies}.")

def get_top_actor():
    top_actor = (Actor.objects.prefetch_related('starring_movies')
                 .annotate(movie_count=Count('starring_movies'),avg_rating=Avg('starring_movies__rating'))
                 .order_by('-movie_count','full_name')).first()



    if not top_actor or not top_actor.movie_count:
        return ''

    movies_title = ', '.join(t.title for t in top_actor.starring_movies.all())
    return f"Top Actor: {top_actor.full_name}, starring in movies: {movies_title}, movies average rating: {top_actor.avg_rating:.1f}"

#==========================

def get_actors_by_movies_count():
    actors = (Actor.objects
              .annotate(movie_count=Count('actors_movies'))
              .order_by('-movie_count','full_name'))[:3]


    if not actors or not actors[0].movie_count:
        return ''


    return '\n'.join(f"{a.full_name}, participated in {a.movie_count} movies" for a in actors)


def get_top_rated_awarded_movie():
    top_movie = (Movie.objects.select_related('starring_actor')
                     .prefetch_related('actors')
                     .filter(is_awarded=True)
                     .order_by('-rating','title')
                     .first()
                     )
    if top_movie is None:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    participating_actor = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ', '.join(participating_actor)

    return (f"Top rated awarded movie: {top_movie.title},"
            f" rating: {top_movie.rating:.1f}."
            f" Starring actor: {starring_actor}."
            f" Cast: {cast}.")




def increase_rating():
    rating_to_update = Movie.objects.filter(is_classic=True,rating__lt=10)
    if not rating_to_update:
        return "No ratings increased."

    update_movies_count = rating_to_update.count()
    rating_to_update.update(rating=F('rating') + 0.1,is_classic=True)

    return f"Rating increased for {update_movies_count} movies."


