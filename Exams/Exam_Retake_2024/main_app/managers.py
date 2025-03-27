from django.db.models import manager, Count


class HouseManager(manager.Manager):

    def get_houses_by_dragons_count(self):
        return (self.annotate(dragons_count=Count('dragons_houses'))
                .order_by('-dragons_count','name'))

