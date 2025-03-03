from datetime import datetime, timedelta

from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=40)




class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

#-----------------------------------

class Song(models.Model):
    title = models.CharField(max_length=100,unique=True)


class Artist(models.Model):
    name = models.CharField(max_length=100,unique=True)
    songs = models.ManyToManyField(Song, related_name='artists')

#------------------------------------------------

class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)


class Review(models.Model):
    description  = models.TextField(max_length=200)
    rating = models.SmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

#----------------------------------------------------

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10,unique=True)
    issue_date = models.DateField()
    driver = models.OneToOneField(
        Driver,
        on_delete=models.CASCADE,
        related_name='license'
    )


    def expiration_date(self):
        expiration_date = self.issue_date + timedelta(days=365)
        return expiration_date

    def __str__(self):
        return f"License with number: {self.license_number} expires on {self.expiration_date()}!"




class Owner(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'



class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='cars',
        blank=True,
        null=True
    )



class Registration(models.Model):
    registration_number = models.CharField(max_length=10, unique=True)
    registration_date  = models.DateField(null=True, blank=True)
    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
        related_name='registration',
        blank=True,
        null=True

    )
#--- from Dean
# class Owner(models.Model):
#     name = models.CharField(
#         max_length=50,
#     )
#
#
# class Car(models.Model):
#     model = models.CharField(
#         max_length=50,
#     )
#     year = models.PositiveIntegerField()
#     owner = models.ForeignKey(
#         Owner,
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#         related_name="cars"
#     )
#
#
# class Registration(models.Model):
#     registration_number = models.CharField(
#         max_length=10,
#         unique=True,
#     )
#     registration_date = models.DateField(
#         blank=True,
#         null=True,
#     )
#     car = models.OneToOneField(
#         Car,
#         on_delete=models.CASCADE,
#         related_name="registration",
#         blank=True,
#         null=True,
#     )
#
#



