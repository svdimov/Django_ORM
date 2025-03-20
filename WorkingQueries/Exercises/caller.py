import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from typing import List
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from django.db.models import Case, When, Value, CharField, QuerySet
from main_app.choises import LaptopBrand, OperationSystemType, DifficultyChoices, WorkoutTypeChoices
from populate import populate_model_with_data


# Create and check models

def show_highest_rated_art() -> str:
    rate = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{rate.art_name} is the highest-rated art with a {rate.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())


# def show_the_most_expensive_laptop() -> str:
#     laptop = Laptop.objects.order_by('-price', '-id').first()
#
#     return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"
#
#
# def bulk_create_laptops(args: List[Laptop]) -> None:
#     Laptop.objects.bulk_create(args)
#
#
# def update_to_512_GB_storage() -> None:
#     Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)
#
#
# def update_to_16_GB_memory() -> None:
#     Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)
#
#
# def update_operation_systems() -> None:
#     Laptop.objects.update(
#         operation_system=Case(
#             When(brand='Asus', then=Value(OperationSystemType.Windows)),
#             When(brand="Apple", then=Value(OperationSystemType.MacOS)),
#             When(brand__in=['Dell', 'Acer'], then=Value(OperationSystemType.Linux)),
#             When(brand='Lenovo', then=Value(OperationSystemType.Chrome_OS)),
#         )
#     )
#
#
# def delete_inexpensive_laptops() -> None:
#     Laptop.objects.filter(price__lt=1200).delete()


# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)

def show_the_most_expensive_laptop() -> str:
    laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=[LaptopBrand.Asus, LaptopBrand.Lenovo]).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=[LaptopBrand.Apple, LaptopBrand.Dell, LaptopBrand.Acer]).update(memory=16)


def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopBrand.Asus, then=Value(OperationSystemType.Windows)),
            When(brand=LaptopBrand.Apple, then=Value(OperationSystemType.MacOS)),
            When(brand__in=[LaptopBrand.Dell, LaptopBrand.Acer], then=Value(OperationSystemType.Linux)),
            When(brand=LaptopBrand.Lenovo, then=Value(OperationSystemType.Chrome_OS)),
        )
    )


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()


# =================================
def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title='no title ').update(games_lost=25)


def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__in=[2399, 2300]).update(title='IM')


def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__in=[2299, 2200]).update(title='FM')


def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__in=[2199, 0]).update(title='regular player')


# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())
#
# ===================================================


def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
            When(meal_type='Breakfast', then=Value('Gordon Ramsay')),
            When(meal_type='Lunch', then=Value('Julia Child')),
            When(meal_type='Dinner', then=Value('Jamie Oliver')),
            When(meal_type='Snack', then=Value('Thomas Keller')),

        )
    )


def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type='Breakfast', then=Value("10 minutes")),
            When(meal_type='Lunch', then=Value("12 minutes")),
            When(meal_type='Dinner', then=Value("15 minutes")),
            When(meal_type='Snack', then=Value("5 minutes")),

        )
    )


def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)


def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)


def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()
#
# # Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)
#
#
#

def show_hard_dungeons() -> str:
    dungeon = Dungeon.objects.filter(difficulty=DifficultyChoices.Hard).order_by('-location')

    return '\n'.join(f"{d.name}"
                     f" is guarded by {d.boss_name}"
                     f" who has {d.boss_health}"
                     f" health points!" for d in dungeon)


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)


def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DifficultyChoices.Easy, then=Value('The Erased Thombs')),
            When(difficulty=DifficultyChoices.Medium, then=Value('The Coral Labyrinth')),
            When(difficulty=DifficultyChoices.Hard, then=Value('The Lost Haunt')),
        )
    )


def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(difficulty=DifficultyChoices.Easy).update(boss_health=500)


def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DifficultyChoices.Easy, then=Value(25)),
            When(difficulty=DifficultyChoices.Medium, then=Value(50)),
            When(difficulty=DifficultyChoices.Hard, then=Value(75)),
        )
    )


def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value("1000 Gold")),
            When(location__startswith='E', then=Value("New dungeon unlocked")),
            When(location__endswith='s', then=Value("Dragonheart Amulet")),
        )
    )


def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )


# dungeon1 = Dungeon(
#     name="Dungeon 1",
#     boss_name="Boss 1",
#     boss_health=1000,
#     recommended_level=75,
#     reward="Gold",
#     location="Eternal Hell",
#     difficulty="Hard",
# )
#
# dungeon2 = Dungeon(
#     name="Dungeon 2",
#     boss_name="Boss 2",
#     boss_health=400,
#     recommended_level=25,
#     reward="Experience",
#     location="Crystal Caverns",
#     difficulty="Easy",
# )
#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)
#
#


def show_workouts() -> str:
    workout = Workout.objects.filter(
        workout_type__in=[WorkoutTypeChoices.Calisthenics, WorkoutTypeChoices.CrossFit]
    ).order_by('-difficulty')

    return '\n'.join(f"{w.name}"
                     f" from {w.workout_type}"
                     f" type has {w.difficulty}"
                     f" difficulty!" for w in workout)


def get_high_difficulty_cardio_workouts() -> QuerySet:
    return Workout.objects.filter(workout_type=WorkoutTypeChoices.Cardio, difficulty='High').order_by('instructor')


def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoices.Cardio, then=Value('John Smith')),
            When(workout_type=WorkoutTypeChoices.Strength, then=Value('Michael Williams')),
            When(workout_type=WorkoutTypeChoices.Yoga, then=Value('Emily Johnson')),
            When(workout_type=WorkoutTypeChoices.CrossFit, then=Value('Sarah Davis')),
            When(workout_type=WorkoutTypeChoices.Calisthenics, then=Value('Chris Heria')),
        )
    )


def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
        )
    )
def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=
                            [WorkoutTypeChoices.Strength,WorkoutTypeChoices.Calisthenics]
                            ).delete()


# # Create two Workout instances
# workout1 = Workout.objects.create(
#     name="Push-Ups",
#     workout_type="Calisthenics",
#     duration="10 minutes",
#     difficulty="Intermediate",
#     calories_burned=200,
#     instructor="Bob"
# )
#
# workout2 = Workout.objects.create(
#     name="Running",
#     workout_type="Cardio",
#     duration="30 minutes",
#     difficulty="High",
#     calories_burned=400,
#     instructor="Lilly"
# )
#
# # Run the functions
# print(show_workouts())
#
# high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
# for workout in high_difficulty_cardio_workouts:
#     print(f"{workout.name} by {workout.instructor}")
#
# set_new_instructors()
# for workout in Workout.objects.all():
#     print(f"Instructor: {workout.instructor}")
#
# set_new_duration_times()
# for workout in Workout.objects.all():
#     print(f"Duration: {workout.duration}")
#

Dungeon.objects.update(name='Dungeon')