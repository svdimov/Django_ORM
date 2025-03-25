
from django.db.models import manager, Count




class AuthorManager(manager.Manager):
    def get_authors_by_article_count(self):

        return (self.annotate(article_count=Count('articles_authors'))
                .order_by('-article_count','email'))

