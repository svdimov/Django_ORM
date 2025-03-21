from django.db.models import Manager, Count, manager, QuerySet

from django.db import models


class ProfileManager(manager.Manager):
    def get_regular_customers(self)->QuerySet:

        return self.annotate(order_count=Count('order')).filter(order_count__gt=2).order_by('-order_count')



