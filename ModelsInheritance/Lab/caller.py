import os
from datetime import date
from tkinter.font import names

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions



from main_app.models import Animal, Mammal, Bird, Reptile, Event

# Animal.objects.create(name="Nemo", species="Clownfish", birth_date="2019-04-10", sound="Bubbles")
# Mammal.objects.create(name="Fluffy", species="Orangutan", birth_date="2018-02-10", sound="Chomps", fur_color="Reddish-brown")
# Bird.objects.create(name="Robby", species="American Robin", birth_date="2021-03-20", sound="Chirp", wing_span=28.50)
# Reptile.objects.create(name="Python", species="Ball Python", birth_date="2019-07-01", sound="Hiss", scale_type="Smooth")
#
# animals = Animal.objects.all()
# for a in animals:
#     print(f"{a.name}: {a.species}.")
#
#=====================================================
from main_app.models import ZooKeeper, Veterinarian

# Keep the data from the previous exercise, so you can reuse it

# zookeeper = ZooKeeper.objects.create(first_name="Peter", last_name="Johnson", phone_number="0899524265", specialty="Mammals")
# mammal = Mammal.objects.get(name="Fluffy")
# zookeeper.managed_animals.add(mammal)
# veterinarian = Veterinarian.objects.create(first_name="Dr. Michael", last_name="Smith", phone_number="9876543210", license_number="VET12345")
#
# zookeeper_from_db = ZooKeeper.objects.first()
# print(f"{zookeeper_from_db.first_name} {zookeeper_from_db.last_name} is a ZooKeeper.")
#
# veterinarian_from_db = Veterinarian.objects.first()
# print(f"{veterinarian_from_db.first_name} {veterinarian_from_db.last_name} is a Veterinarian.")
#
#


from datetime import date

# Create an instance of Animal


# Usage in a model

# Example Usage
event = Event(name="Conference", date_range=("2025-03-01", "2025-03-05"))
event.save()
