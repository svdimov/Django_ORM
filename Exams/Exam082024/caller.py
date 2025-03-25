import os


import django
from django.db.models import Q, Count, Sum, F, Avg, Case, When, Value, FloatField
from django.utils import timezone

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft


# Create queries within functions

def get_astronauts(search_string=None):
    if search_string is None:
        return ''


    q_name = Q(name__icontains=search_string)
    q_phone = Q(phone_number__icontains=search_string)


    astronauts = (Astronaut.objects
                  .filter(q_name | q_phone)
                  .order_by('name'))
    if not astronauts.exists():
        return ''

    return '\n'.join(
        f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}"
        for a in astronauts
    )


def get_top_astronaut():
    astronauts = ((Astronaut.objects
                   .annotate(number_missions=Count('mission_astronauts'))
                   .order_by('-number_missions', 'phone_number'))
                  .first())
    if not astronauts or astronauts.number_missions == 0:
        return "No data."

    return f"Top Astronaut: {astronauts.name} with {astronauts.number_missions} missions."


def get_top_commander():
    astronauts = (((Astronaut.objects.
                  annotate(count_commander=Count('mission_commanders')))
                  .order_by('-count_commander', 'phone_number'))
                  .first())
    if not astronauts or astronauts.count_commander == 0:
        return "No data."

    return f"Top Commander: {astronauts.name} with {astronauts.count_commander} commanded missions."

#==============================================================================

def get_last_completed_mission():
    last_completed_mission = (Mission.objects
                              .filter(status=Mission.StatusChoices.Completed)
                              .order_by('-launch_date').first())

    if not last_completed_mission:
        return "No data."

    commander_names = 'TBA' if not last_completed_mission.commander else last_completed_mission.commander.name
    astronauts_names = last_completed_mission.astronauts.order_by('name').values_list('name', flat=True)
    number_walks = last_completed_mission.astronauts.aggregate(number_spacewalk=Sum('spacewalks'))[
                       'number_spacewalk'] or 0

    return (f"The last completed mission is: {last_completed_mission.name}. "
            f"Commander: {commander_names}. "
            f"Astronauts: {', '.join(astronauts_names)}. "
            f"Spacecraft: {last_completed_mission.spacecraft.name}. "
            f"Total spacewalks: {number_walks}.")




def get_most_used_spacecraft():
    most_used_spacecraft = (Spacecraft.objects
                            .annotate(number_missions=Count('mission_spacecrafts'))
                            .order_by('-number_missions', 'name')
                            .first())

    if not most_used_spacecraft or most_used_spacecraft.number_missions == 0:
        return "No data."

    num_astronauts = (Astronaut.objects
                      .filter(mission_astronauts__spacecraft=most_used_spacecraft)
                      .distinct().count())

    return (f"The most used spacecraft is: {most_used_spacecraft.name}, "
            f"manufactured by {most_used_spacecraft.manufacturer}, "
            f"used in {most_used_spacecraft.number_missions} "
            f"missions, astronauts on missions: {num_astronauts}.")

# def get_most_used_spacecraft():



def decrease_spacecrafts_weight():



        unique_spacecrafts = (Spacecraft.objects
                              .annotate(num_planned=Count('mission_spacecrafts',
                                                          filter=Q(mission_spacecrafts__status='Planned')))
                              .filter(weight__gte=200, num_planned__gt=0)
                              .distinct())

        num_of_spacecrafts_affected = unique_spacecrafts.count()

        if num_of_spacecrafts_affected == 0:
            return "No changes in weight."

        # Safeguard to prevent weight from dropping below 0
        unique_spacecrafts.update(
            weight=Case(
                When(weight__gte=200, then=F('weight') - 200),
                default=Value(0.0),
                output_field=FloatField()
            )
        )

        avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']


        return f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
