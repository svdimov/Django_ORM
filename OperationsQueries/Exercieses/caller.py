import os
from decimal import Decimal

import django

from main_app.choices import RoomTypeChoices, CharacterTypeChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db import connection
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from main_app.choices import RoomTypeChoices, CharacterTypeChoices
from django.db.models import QuerySet, F


# Create queries within functions

def create_pet(name: str, species: str):
    pet = Pet.objects.create(name=name, species=species)

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(name=name, origin=origin, age=age, description=description,
                                       is_magical=is_magical)
    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(f"{l.name} has a population of "
                     f"{l.population}!" for l in locations
                     )


def new_capital() -> None:
    Location.objects.filter(id=Location.objects.first().id).update(is_capital=True)


def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        percentage = Decimal(str(sum(int(c) for c in str(car.year)) / 100))
        discount = car.price * percentage
        car.price_with_discount = car.price - discount

    Car.objects.bulk_update(cars, ['price_with_discount'])


def get_recent_cars():
    cars = Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')
    return cars


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(f"Task - "
                     f"{t.title} needs to be done until "
                     f"{t.due_date}!" for t in tasks)


def complete_odd_tasks() -> None:
    task = Task.objects.all()
    odd_task = []
    for t in task:
        if t.id % 2 != 0:
            t.is_finished = True
            odd_task.append(t)

    Task.objects.bulk_update(odd_task, ['is_finished'])
    #
    # TaskEncoder.objects.filter(id__mod=2, id__gt=0).update(is_finished=True)


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join(chr(ord(t) - 3) for t in text)
    Task.objects.filter(title=task_title).update(description=encoded_text)


def add_date_hotel():
    data1 = HotelRoom(
        room_number=401,
        room_type='Standard',
        capacity=2,
        amenities='Tv',
        price_per_night=100

    )
    data2 = HotelRoom(
        room_number=401,
        room_type='Deluxe',
        capacity=3,
        amenities='Wi-Fi',
        price_per_night=200

    )
    data3 = HotelRoom(
        room_number=601,
        room_type='Deluxe',
        capacity=6,
        amenities='Jacuzzi',
        price_per_night=400

    )

    HotelRoom.objects.bulk_create([data1, data2, data3])


def get_deluxe_rooms() -> str:
    rooms = HotelRoom.objects.filter(room_type=RoomTypeChoices.Deluxe)
    even_numbers = []
    for r in rooms:
        if r.id % 2 == 0:
            even_numbers.append(r)

    return '\n'.join(f"Deluxe room with number "
                     f"{r.room_number} costs "
                     f"{r.price_per_night}$ per night!" for r in even_numbers)


def increase_room_capacity():
    rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')

    previous_room: HotelRoom = None

    for r in rooms:
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r

        r.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


def update_characters() -> None:
    Character.objects.filter(class_name=CharacterTypeChoices.Mage).update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )
    Character.objects.filter(class_name=CharacterTypeChoices.Warrior).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )
    Character.objects.filter(class_name__in=[CharacterTypeChoices.Scout, CharacterTypeChoices.Assassin]).update(
        inventory="The inventory is empty",
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_items = None
    if first_character.class_name in [CharacterTypeChoices.Mage, CharacterTypeChoices.Scout]:
        fusion_items = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [CharacterTypeChoices.Warrior, CharacterTypeChoices.Assassin]:
        fusion_items = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=CharacterTypeChoices.Fusion,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=fusion_items,
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory="The inventory is empty").delete()
