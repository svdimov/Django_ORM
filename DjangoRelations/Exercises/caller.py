import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car
from django.db.models import QuerySet, Avg
from datetime import datetime, timedelta, date

# Create queries within functions

def show_all_authors_with_their_books()->str :
    authors = Author.objects.all().order_by('id')
    result = []

    for author in authors :
        books = Book.objects.filter(author=author)
        if not books :
            continue

        result.append(f"{author.name} has written"
                         f" - {', '.join(b.title for b in books)}!")

    return '\n'.join(result)


def delete_all_authors_without_books()->None :
    # books = Book.objects.filter(author__book__isnull=True).delete()
    Author.objects.filter(book__isnull=True).delete()


# Create authors
# author1 = Author.objects.create(name="J.K. Rowling")
# author2 = Author.objects.create(name="George Orwell")
# author3 = Author.objects.create(name="Harper Lee")
# author4 = Author.objects.create(name="Mark Twain")
#
# # Create books associated with the authors
# book1 = Book.objects.create(
#     title="Harry Potter and the Philosopher's Stone",
#     price=19.99,
#     author=author1
# )
# book2 = Book.objects.create(
#     title="1984",
#     price=14.99,
#     author=author2
# )
#
# book3 = Book.objects.create(
#     title="To Kill a Mockingbird",
#     price=12.99,
#     author=author3
# )
#
# # Display authors and their books
# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
#
# # Delete authors without books
# delete_all_authors_without_books()
# print(Author.objects.count())
#
#
#-------------------------------------------------

def add_song_to_artist(artist_name: str, song_title: str)->None :
    artist_name = Artist.objects.get(name=artist_name)
    song_name = Song.objects.get(title=song_title)

    artist_name.songs.add(song_name)

def get_songs_by_artist(artist_name: str) :
    artist = Artist.objects.get(name=artist_name)

    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) :
    artist = Artist.objects.get(name=artist_name)
    current_song = Song.objects.get(title=song_title)
    artist.songs.remove(current_song)

# # Create artists
# artist1 = Artist.objects.create(name="Daniel Di Angelo")
# artist2 = Artist.objects.create(name="Indila")
# # Create songs
# song1 = Song.objects.create(title="Lose Face")
# song2 = Song.objects.create(title="Tourner Dans Le Vide")
# song3 = Song.objects.create(title="Loyalty")
#
# # Add a song to an artist
# add_song_to_artist("Daniel Di Angelo", "Lose Face")
# add_song_to_artist("Daniel Di Angelo", "Loyalty")
# add_song_to_artist("Indila", "Tourner Dans Le Vide")
#
# # Get all songs by a specific artist
# songs = get_songs_by_artist("Daniel Di Angelo")
# for song in songs:
#     print(f"Daniel Di Angelo: {song.title}")
#
# # Get all songs by a specific artist
# songs = get_songs_by_artist("Indila")
# for song in songs:
#     print(f"Indila: {song.title}")
#
# # Remove a song from an artist
# remove_song_from_artist("Daniel Di Angelo", "Lose Face")
#
# # Check if the song is removed
# songs = get_songs_by_artist("Daniel Di Angelo")
#
# for song in songs:
#     print(f"Songs by Daniel Di Angelo after removal: {song.title}")

#-------------------------------------------------


def calculate_average_rating_for_product_by_name(product_name: str)->float :
    # product = Product.objects.annotate(
    #     avg_review_score=Avg('reviews__rating')
    # ).get(name=product_name)
    # return product
    product = Product.objects.get(name=product_name)
    rev = product.reviews.all()
    avg_rating = sum(r.rating for r in rev) / len(rev)

    return avg_rating


def get_reviews_with_high_ratings(threshold: int)->QuerySet :

    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews()->QuerySet :

    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews()->None :
    Product.objects.filter(reviews__isnull=True).delete()


# Create some products
# product1 = Product.objects.create(name="Laptop")
# product2 = Product.objects.create(name="Smartphone")
# product3 = Product.objects.create(name="Headphones")
# product4 = Product.objects.create(name="PlayStation 5")
#
# # Create some reviews for products
# review1 = Review.objects.create(description="Great laptop!", rating=5, product=product1)
# review2 = Review.objects.create(description="The laptop is slow!", rating=2, product=product1)
# review3 = Review.objects.create(description="Awesome smartphone!", rating=5, product=product2)
#
# # Run the function to get products without reviews
# products_without_reviews = get_products_with_no_reviews()
# print(f"Products without reviews: {', '.join([p.name for p in products_without_reviews])}")
# # Run the function to delete products without reviews
# delete_products_without_reviews()
# print(f"Products left: {Product.objects.count()}")
#
# # Calculate and print the average rating
# print(calculate_average_rating_for_product_by_name("Laptop"))





def calculate_licenses_expiration_dates()->str :
    licenses = DrivingLicense.objects.all().order_by('-license_number')

    return '\n'.join(str(l) for l in licenses)

def get_drivers_with_expired_licenses(due_date: date) :
    exp_licenses = DrivingLicense.objects.filter(issue_date__gt=due_date - timedelta(days=365))

    return [l.driver for l in exp_licenses ]

# Create drivers
# driver1 = Driver.objects.create(first_name="Tanya", last_name="Petrova")
# driver2 = Driver.objects.create(first_name="Ivan", last_name="Yordanov")
#
# # Create licenses associated with drivers
# license1 = DrivingLicense.objects.create(license_number="123", issue_date=date(2022, 10, 6), driver=driver1)
#
# license2 = DrivingLicense.objects.create(license_number="456", issue_date=date(2022, 1, 1), driver=driver2)
#
# # Calculate licenses expiration dates
# expiration_dates = calculate_licenses_expiration_dates()
# print(expiration_dates)
#
# # Get drivers with expired licenses
# drivers_with_expired_licenses = get_drivers_with_expired_licenses(date(2023, 1, 1))
#
# for driver in drivers_with_expired_licenses:
#     print(f"{driver.first_name} {driver.last_name} has to renew their driving license!")
#
#-------------------------------------------------------------

def register_car_by_owner(owner: Owner) :
    car = Car.objects.filter(registration__isnull=True).first()
    reg = Registration.objects.filter(car__isnull=True).first()
    car.owner = owner
    car.registration = reg
    car.save()

    reg.registration_date = datetime.today()
    reg.car = car
    reg.save()

    return (f"Successfully registered {car.model}"
            f" to {owner.name} "
            f"with registration number {reg.registration_number}.")
#from Dean
# def register_car_by_owner(owner: Owner) -> str:
#     car = Car.objects.filter(registration__isnull=True).first()
#     registration = Registration.objects.filter(car__isnull=True).first()
#
#     car.owner = owner
#     car.registration = registration
#
#     car.save()
#
#     registration.registration_date = datetime.today()
#     registration.car = car
#
#     registration.save()
#
#     return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."




















