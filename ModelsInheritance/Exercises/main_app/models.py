from datetime import date, timedelta
from enum import StrEnum

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet

from main_app.fields import StudentIDField, MaskedCreditCardField


# Create your models here.

class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)


# ======================================================

class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)


class Message(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self) -> None:
        self.is_read = True

    def reply_to_message(self, reply_content: str):
        new_message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )

        new_message.save()
        return new_message

    def forward_message(self, receiver: UserProfile):
        new_message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )
        new_message.save()
        return new_message


# ===================================================


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


# ======================================================

# class CreditCard(models.Model):
#     card_owner = models.CharField(max_length=100)
#     card_number = MaskedCreditCardField(max_length=100)
#
class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100,
    )
    card_number = MaskedCreditCardField(max_length=100)


# =====================================================


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(decimal_places=2, max_digits=10)

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs) -> str:
        self.clean()
        super().save(*args, **kwargs)
        return f"Room {self.number} created successfully"


class ReservationTypes(StrEnum):
    REGULAR = "Regular"
    SPECIAL = "Special"


class BaseReservation(models.Model):
    class Meta:
        abstract = True
    reservation_type = None

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self) -> int:
        period = (self.end_date - self.start_date).days

        return period

    def calculate_total_cost(self):  # Chek Error
        total_cost = round(self.room.price_per_night * self.reservation_period(), 2)
        return total_cost

    def get_overlapping_reservations(self, start_date: date, end_date: date)->QuerySet :
        return self.__class__.objects.filter(
            room=self.room,
            end_date__gte=start_date,
            start_date__lte=end_date,
        )

    @property
    def is_available(self):
        reservations = self.get_overlapping_reservations(self.start_date, self.end_date)
        return not reservations.exists()

    def clean(self):

        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"{self.reservation_type} reservation for room {self.room.number}"

class RegularReservation(BaseReservation):
    reservation_type = ReservationTypes.REGULAR.value




class SpecialReservation(BaseReservation):
    reservation_type = ReservationTypes.SPECIAL.value

    def extend_reservation(self,days: int) :
        new_end_date = self.end_date + timedelta(days=days)
        reservations = self.get_overlapping_reservations(self.start_date, new_end_date)

        if reservations:
            raise ValidationError("Error during extending reservation")

        self.end_date = new_end_date
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"





