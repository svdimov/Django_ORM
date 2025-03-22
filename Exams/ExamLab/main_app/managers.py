from django.db import models
from django.db.models import manager, Count



class DirectorManager(manager.Manager):

    def get_directors_by_movies_count(self):

        return self.annotate(number_of_movies=Count('director_movies'))\
            .order_by('-number_of_movies', 'full_name')


