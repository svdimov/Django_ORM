from django.db.models import manager, Count


class PublisherManager(manager.Manager):
    def get_publishers_by_books_count(self):

        return (self.annotate(books_count=Count('books_publisher'))
                .order_by('-books_count','name'))
