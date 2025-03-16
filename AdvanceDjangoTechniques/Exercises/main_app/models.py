from decimal import Decimal

from django.core.validators import EmailValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.db.models.lookups import Regex

from main_app.validators import ValidateName, ValidatePhoneNumber, validate_name


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100,
                            validators=[ValidateName(message='Name can only contain letters and spaces')])
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message='Age must be greater than or equal to 18')])
    email = models.EmailField(
        error_messages={'invalid': "Enter a valid email address"}
    )
    phone_number = models.CharField(max_length=13, validators=[
        ValidatePhoneNumber(message="Phone number must start with '+359' followed by 9 digits")])
    website_url = models.URLField(
        error_messages={'invalid': "Enter a valid URL"}
    )


# ======================================
class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'

    author = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(
            5, message="Author must be at least 5 characters long")])
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(
            6, message="ISBN must be at least 6 characters long")])


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'

    director = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(
            8, message="Director must be at least 8 characters long")]
    )


class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'

    artist = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(9, message="Artist must be at least 9 characters long")]
    )


# ========================================================

class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2')

    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def calculate_tax(self) -> Decimal:
        return self.price * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self) -> str:
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    PRICE_INCREASE_PERCENT: Decimal = Decimal('0.20')
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.5')

    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        discounted_price = Decimal(str(self.price)) * (1 + self.PRICE_INCREASE_PERCENT)
        return discounted_price

    def format_product_name(self) -> str:
        return f"Discounted Product: {self.name}"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++

class RechargeEnergyMixin:

    def recharge_energy(self, amount: int):
        self.energy += amount
        if self.energy > 100:
            self.energy = 100
        self.save()

class Hero(models.Model, RechargeEnergyMixin):
    MIN_ENERGY: int = 1

    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    # @property
    # def required_energy_message(self) -> str:
    #     return ""
    #
    # @property
    # def successful_ability_use_message(self) -> str:
    #     return ""
    #
    # def use_ability(self):
    #     if self.energy < self.ABILITY_ENERGY_REQUIRED:
    #         return self.required_energy_message
    #
    #     if self.energy - self.ABILITY_ENERGY_REQUIRED > 0:
    #         self.energy -= self.ABILITY_ENERGY_REQUIRED
    #     else:
    #         self.energy = self.MIN_ENERGY
    #
    #     self.save()
    #
    #     return self.successful_ability_use_message


class SpiderHero(Hero):
    UNITS_DECREASES = 80

    class Meta:
        proxy = True

    def swing_from_buildings(self) -> str:
        if self.energy < self.UNITS_DECREASES:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        self.energy -= self.UNITS_DECREASES

        if self.energy <= 0:
            self.energy = self.MIN_ENERGY


        self.save()
        return f"{self.name} as Spider Hero swings from buildings using web shooters"


class FlashHero(Hero):
    UNITS_DECREASES = 65

    class Meta:
        proxy = True

    def run_at_super_speed(self) -> str:
        if self.energy < self.UNITS_DECREASES:
            return f"{self.name} as Flash Hero needs to recharge the speed force"

        self.energy -= self.UNITS_DECREASES

        if self.energy <= 0:
            self.energy = self.MIN_ENERGY


        self.save()
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"
