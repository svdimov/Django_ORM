import os
import django
from django.db.models import Q, Count, Avg



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article
# Create queries within functions

# def get_authors(search_name=None, search_email=None):
#     q_name = Q(full_name__icontains=search_name)
#     q_email = Q(email__icontains=search_email)
#     if search_name is not None and search_email is not None:
#         query = Q(q_name) & Q(q_email)
#     elif search_name is not None:
#         query = Q(q_name)
#     elif search_email is not None:
#         query = Q(q_email)
#     else:
#         return ''
#     author = Author.objects.filter(query).order_by('-full_name')
#     if  not author:
#         return ''
#
#     return '\n'.join(f'Author: '
#                      f'{a.full_name}, '
#                      f'email: {a.email}, '
#                      f'status: {a.is_banned}' for a in author)
#
#
# def get_top_publisher():
#     author = (Author.objects.annotate(count_articles=Count('articles_authors'))
#               .order_by('-count_articles', 'email')
#               .first())
#     if author is None or author.count_articles==0:
#         return ''
#
#     return f"Top Author: {author.full_name} with {author.count_published} published articles."
#
#
# def get_top_reviewer():
#     author = (Author.objects.annotate(count_reviewer=Count('reviews_authors'))
#               .order_by('-count_reviewer', 'email')
#               .first())
#     if author is None or author.count_reviewer==0:
#         return ''
#
#     return  f"Top Reviewer: {author.full_name} with {author.count_reviewer} published reviews."

from django.db.models import Q, Count

def get_authors(search_name=None, search_email=None):
    q_name = Q(full_name__icontains=search_name)  # $ Incorrect field name. Should be "full_name" not "name".
    q_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = q_name & q_email
    elif search_name is not None:
        query = q_name
    elif search_email is not None:  # $ Missing condition. Should check if search_email is not None.
        query = q_email
    else:
        return ''

    authors = Author.objects.filter(query).order_by('-full_name')  # $ Variable should be "authors" not "author" (plural for queryset).
    if not authors:
        return ''

    return '\n'.join(
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"  # $ Correct status formatting.
        for a in authors
    )


def get_top_publisher():
    author = (Author.objects.annotate(count_articles=Count('articles_authors'))
              .order_by('-count_articles', 'email')
              .first())
    if author is None or author.count_articles == 0:  # $ Check if count_articles is 0.
        return ''

    return f"Top Author: {author.full_name} with {author.count_articles} published articles."  # $ Wrong attribute name. Should be "count_articles", not "count_published".


def get_top_reviewer():
    author = (Author.objects.annotate(count_reviews=Count('reviews_authors'))  # $ Wrong alias. Should be "count_reviews" instead of "count_reviewer".
              .order_by('-count_reviews', 'email')
              .first())
    if author is None or author.count_reviews == 0:  # $ Check if count_reviews is 0.
        return ''

    return f"Top Reviewer: {author.full_name} with {author.count_reviews} published reviews."  # $ Wrong attribute name. Should be "count_reviews", not "count_reviewer".

#===================================================================



def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if not latest_article:
        return ""

    authors = latest_article.authors.order_by('full_name').values_list('full_name', flat=True)
    num_reviews = latest_article.reviews_articles.count()
    avg_rating = latest_article.reviews_articles.aggregate(avg_rating=Avg('rating'))['avg_rating']
    avg_rating = f"{avg_rating:.2f}" if avg_rating is not None else "0.00"

    return (f"The latest article is: {latest_article.title}. Authors: {', '.join(authors)}. "
            f"Reviewed: {num_reviews} times. Average Rating: {avg_rating}.")


def get_top_rated_article():
    top_article = (Article.objects.annotate(
        avg_rating=Avg('reviews_articles__rating'),
        num_reviews=Count('reviews_articles')
    ).filter(num_reviews__gt=0)
                   .order_by('-avg_rating','title')
                   .first())

    if not top_article:
        return ''

    return (f"The top-rated article is: "
            f"{top_article.title}, with an average rating of "
            f"{top_article.avg_rating:.2f}, reviewed "
            f"{top_article.num_reviews} times.")





def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.filter(email=email).first()

    if not author:
        return "No authors banned."
    num_reviews = author.reviews_authors.count()
    author.reviews_authors.all().delete()

    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."









































