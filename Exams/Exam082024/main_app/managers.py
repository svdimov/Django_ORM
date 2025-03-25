
from django.db.models import manager, Count


class AstronautManager(manager.Manager):
    def get_astronauts_by_missions_count(self):

        return (self.annotate(missions_count=Count('mission_astronauts'))
                .order_by('-missions_count','phone_number'))
