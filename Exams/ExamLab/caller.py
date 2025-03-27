import os
import django
from django.db.models import Q, Count, Avg, F, Case, When, Value

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    q_name = Q(full_name__icontains=search_name)
    q_nationality = Q(nationality__icontains=search_nationality)
    if search_name is not None and search_nationality is not None:
        query = q_name & q_nationality
    elif search_name is not None:
        query = q_name
    else:
        query = q_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    return '\n'.join(f"Director: {d.full_name}, "
                     f"nationality: {d.nationality}, "
                     f"experience: {d.years_of_experience}"
                     for d in directors)

def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if director is None:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.number_of_movies}."


def get_top_actor():
    top_actor = ((Actor.objects
                 .annotate(movies_count=Count('starring_movies')
                           ,movies_avg_rating=Avg('starring_movies__rating'))
                 .order_by('-movies_count','full_name'))
                 .first())


    if top_actor is None or top_actor.movies_count == 0:
        return ''

    movie_title = top_actor.starring_movies.values_list('title', flat=True)

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join(movie_title)}, "
            f"movies average rating: {top_actor.movies_avg_rating:.1f}")


#+++++++++++++++++++++++++++++++++++++++


def get_actors_by_movies_count():
    top_tree_actors = Actor.objects\
                          .annotate(movies_count=Count('actors_movies'))\
                          .order_by('-movies_count', 'full_name')[:3]

    if not top_tree_actors or not top_tree_actors[0].movies_count:
        return ''

    return '\n'.join(f"{actor.full_name}, participated in {actor.movies_count} movies" for actor in top_tree_actors)


def get_top_rated_awarded_movie():

    movies = Movie.objects.filter(is_awarded=True).order_by('-rating','title').first()

    if movies is None:
        return ''

    starring_actor_full_name = movies.starring_actor.full_name if movies.starring_actor else 'N/A'
    cast = ', '.join(movies.actors.values_list('full_name', flat=True))

    return (f"Top rated awarded movie: {movies.title}, "
            f"rating: {movies.rating}. "
            f"Starring actor: {starring_actor_full_name}. "
            f"Cast: {cast}.")




def increase_rating():
    movies = (Movie.objects
              .filter(is_classic=True,rating__lt=10)
              .update(rating=F('rating')+ 0.1,is_classic=True))

    if not movies:
        return "No ratings increased."

    return f"Rating increased for {movies} movies."

