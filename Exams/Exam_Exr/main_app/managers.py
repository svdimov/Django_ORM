from django.db.models import Manager, Count, manager, QuerySet



class ProfileManager(manager.Manager):
    def get_regular_customers(self)->QuerySet:

        return self.prefetch_related('orders_profiles').annotate(order_count=Count('orders_profiles')).filter(order_count__gt=2).order_by('-order_count')



