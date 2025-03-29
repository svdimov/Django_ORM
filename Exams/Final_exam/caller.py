import os
from datetime import date

import django
from django.db import connection
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book


# Create queries within functions

def populate_db():
    # Publishers
    epic_reads = Publisher.objects.create(
        name='Epic Reads',
        established_date=date(1923, 5, 15),
        country='USA',
        rating=4.94
    )
    global_prints = Publisher.objects.create(
        name='Global Prints',
        established_date=date(1800, 1, 1),  # Default date
        country='Australia'
    )
    abrams_books = Publisher.objects.create(
        name='Abrams Books',
        established_date=date(1800, 1, 1),  # Default date
        rating=1.05
    )

    # Authors
    jack_london = Author.objects.create(
        name='Jack London',
        birth_date=date(1876, 1, 12),
        country='USA',
        is_active=False
    )
    craig_richardson = Author.objects.create(name='Craig Richardson')
    ramsey_hamilton = Author.objects.create(name='Ramsey Hamilton')
    luciano_ramalho = Author.objects.create(name='Luciano Ramalho')

    # Books
    book1 = Book.objects.create(
        title='Adventures in Python',
        publication_date=date(2015, 6, 1),
        summary='An engaging and detailed guide to mastering Python.',
        genre=Book.GenreChoice.Non_Fiction,
        price=49.99,
        rating=4.8,
        publisher=epic_reads,
        main_author=craig_richardson
    )
    book1.co_authors.add(ramsey_hamilton)

    book2 = Book.objects.create(
        title='The Call of the Wild',
        publication_date=date(1903, 11, 23),
        summary='A classic fiction adventure story set during the Klondike Gold Rush.',
        genre=Book.GenreChoice.Fiction,
        price=29.99,
        rating=4.9,
        is_bestseller=True,
        publisher=global_prints,
        main_author=jack_london
    )

    book3 = Book.objects.create(
        title='Django World',
        publication_date=date(2025, 1, 1),
        summary='A comprehensive resource for advanced users of Django.',
        genre=Book.GenreChoice.Non_Fiction,
        price=89.99,
        rating=5.0,
        publisher=epic_reads,
        main_author=craig_richardson
    )
    book3.co_authors.add(luciano_ramalho, ramsey_hamilton)

    book4 = Book.objects.create(
        title='Integration Testing',
        publication_date=date(2024, 12, 31),
        summary='A thorough exploration of expert-level testing strategies.',
        genre=Book.GenreChoice.Non_Fiction,
        price=89.99,
        rating=4.89,
        is_bestseller=True,
        publisher=epic_reads,
        main_author=ramsey_hamilton
    )

    book5 = Book.objects.create(
        title='Unit Testing',
        publication_date=date(2025, 2, 1),
        summary='A detailed guide to foundational testing principles.',
        genre=Book.GenreChoice.Non_Fiction,
        price=90.00,
        rating=3.99,
        publisher=epic_reads,
        main_author=craig_richardson
    )
    book5.co_authors.add(ramsey_hamilton)

    return 'Database populated'
def get_publishers(search_string=None):
    if search_string is None:
        return "No search criteria."

    q_name = Q(name__icontains=search_string)
    q_country = Q(country__icontains=search_string)

    publishers = Publisher.objects.filter(q_name | q_country).order_by('-rating', 'name')

    if not publishers.exists():
        return "No publishers found."

    return '\n'.join(f"Publisher: {p.name}, "
                     f"country: {'Unknown' if p.country == 'TBC' else p.country}, "
                     f"rating: {p.rating:.1f}" for p in publishers)


def get_top_publisher():
    publishers = Publisher.objects.get_publishers_by_books_count().first()

    if publishers is None:
        return "No publishers found."

    return f"Top Publisher: {publishers.name} with {publishers.books_count} books."




def get_top_main_author():
    author = (Author.objects
              .annotate(books_count=Count('books_author'), books_avg_rating=Avg('books_author__rating'))
              .filter(books_count__gt=0)  #
              .order_by('-books_count', 'name')
              .first())

    if not author:
        return "No results."


    book_titles = [a.title for a in author.books_author.order_by('title')]


    avg_rating = f"{author.books_avg_rating:.1f}"

    return (f"Top Author: {author.name}, "
            f"own book titles: {', '.join(book_titles)}, "
            f"books average rating: {avg_rating}")






#===================================================================

def get_authors_by_books_count():
    authors = (Author.objects
               .annotate(total_books=Count('books_author') + Count('books_co_authors'))
               .filter(total_books__gt=0)
               .order_by('-total_books', 'name')[:3])

    if not authors:
        return "No results."

    return "\n".join(f"{author.name} authored {author.total_books} books." for author in authors)

def get_top_bestseller():
    bestseller = (Book.objects
             .filter(is_bestseller=True)
             .order_by('-rating', 'title')
             .first())

    if bestseller is None:

        return "No results."

    co_author_name = [b.name for b in bestseller.co_authors.order_by('name')]
    co_author_st = ', '.join(co_author_name) if co_author_name else "N/A"

    return (f"Top bestseller: {bestseller.title}, "
            f"rating: {bestseller.rating:.1f}. "
            f"Main author: {bestseller.main_author.name}. "
            f"Co-authors: {co_author_st}.")

def increase_price():

    books = (Book.objects.
             filter(publication_date__year=2025, rating__gte=4.0)
             .update(price=F('price') * 0.2 + F('price')))
    if not books:
        return "No changes in price."

    return f"Prices increased for {books} books."




