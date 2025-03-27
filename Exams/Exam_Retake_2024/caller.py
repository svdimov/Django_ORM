import os

import django
from django.db.models import Q, F, Case, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import House, Dragon, Quest


# Create queries within functions
def get_houses(search_string=None):
    if not search_string:
        return "No houses match your search."

    q_name = Q(name__startswith=search_string)
    q_moto = Q(motto__startswith=search_string)

    houses = House.objects.filter(q_name | q_moto).order_by('-wins', 'name')

    if not houses.exists():
        return "No houses match your search."

    return '\n'.join(f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}" for h in houses)


def get_most_dangerous_house():
    house_dragons = (House.objects
                     .annotate(num_of_dragons=Count('dragons_houses'))
                     .order_by('-num_of_dragons', 'name').first())

    if not house_dragons or house_dragons.num_of_dragons == 0:
        return "No relevant data."
    ruling = 'ruling' if house_dragons.is_ruling else 'not ruling'

    return (f"The most dangerous house is the House of {house_dragons.name} "
            f"with {house_dragons.num_of_dragons} "
            f"dragons. Currently {ruling} the kingdom.")


def get_most_powerful_dragon():
    dragon = (Dragon.objects
              .annotate(num_quests=Count('quests_dragons'))
              .filter(is_healthy=True)
              .order_by('-power', 'name').first())

    if not dragon:
        return "No relevant data."

    return (f"The most powerful healthy dragon is {dragon.name} "
            f"with a power level of {dragon.power:.1f}, "
            f"breath type {dragon.breath}, "
            f"and {dragon.wins} wins, coming from the house of {dragon.house.name}. "
            f"Currently participating in {dragon.num_quests} quests.")


# ===========================================================================
def update_dragons_data():
    injured_dragons = Dragon.objects.filter(is_healthy=False, power__gt=1.0)

    num_of_dragons_affected = injured_dragons.update(power=F('power') - 0.1, is_healthy=True)

    if num_of_dragons_affected == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    return f"The data for {num_of_dragons_affected} dragon/s has been changed. The minimum power level among all dragons is {min_power:.1f}"



def get_earliest_quest():
    quest = Quest.objects.order_by('start_time').first()

    if quest is None:
        return "No relevant data."

    start_time = quest.start_time
    day = start_time.day
    month = start_time.month
    year = start_time.year

    dragons = quest.dragons.order_by('-power', 'name')
    dragon_names_str = "*".join([dragon.name for dragon in dragons])

    avg_power_level = dragons.aggregate(Avg('power'))['power__avg']
    # avg_power_level = f"{avg_power_level:.2f}" if avg_power_level else "0.00"

    return (
        f"The earliest quest is: {quest.name}, code: {quest.code}, "
        f"start date: {day}.{month}.{year}, host: {quest.host.name}. "
        f"Dragons: {dragon_names_str}. Average dragons power level: {avg_power_level:.2f}")



def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code=quest_code).first()
    if  quest is None:
        return "No such quest."

    wining_dragons = quest.dragons.order_by('-power', 'name').first()

    wining_dragons.wins += 1
    wining_dragons.save()

    winner_house = wining_dragons.house
    winner_house.wins += 1
    winner_house.save()

    quest.delete()

    return (f"The quest: {quest.name} "
            f"has been won by dragon {wining_dragons.name} "
            f"from house {wining_dragons.house.name}. "
            f"The number of wins has been updated as follows: {wining_dragons.wins} "
            f"total wins for the dragon and {wining_dragons.house.wins} "
            f"total wins for the house. The house was awarded with {quest.reward:.2f} coins.")

