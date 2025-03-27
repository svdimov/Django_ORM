import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    q_name = Q(full_name__icontains=search_name)
    q_country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query = q_name & q_country
    elif search_name is not None:
        query = q_name
    else:
        query = q_country

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players:
        return ''

    return '\n'.join(f"Tennis Player: {p.full_name},"
                     f" country: {p.country}, "
                     f"ranking: {p.ranking}" for p in players)


def get_top_tennis_player():
    players = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if players is None:
        return ''

    return f"Top Tennis Player: {players.full_name} with {players.num_wins} wins."


def get_tennis_player_by_matches_count():
    players = (TennisPlayer.objects
               .annotate(mach_count=Count('matches_players'))
               .order_by('-mach_count', 'ranking')
               .first())

    if players is None or players.mach_count == 0:
        return ''

    return f"Tennis Player: {players.full_name} with {players.mach_count} matches played."


# ====================================================================

def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments = (Tournament.objects
                   .prefetch_related('matches_tournament')
                   .annotate(num_matches=Count('matches_tournament'))
                   .filter(surface_type__icontains=surface)
                   .order_by('-start_date'))

    return '\n'.join(f"Tournament: {t.name}, "
                     f"start date: {t.start_date}, "
                     f"matches: {t.num_matches}" for t in tournaments)




def get_latest_match_info():
    latest_match = (Match.objects
                    .order_by('-date_played', '-id')
                    .first())

    if not latest_match:
        return ""

    # player_names = sorted(list(latest_match.players.values_list('full_name', flat=True)))
    player_names = latest_match.players.order_by('full_name').values_list('full_name', flat=True)
    players_str = " vs ".join(player_names)

    winner_name = latest_match.winner.full_name if latest_match.winner else "TBA"


    return (f"Latest match played on: {latest_match.date_played}, "
            f"tournament: {latest_match.tournament.name}, "
            f"score: {latest_match.score}, "
            f"players: {players_str}, "
            f"winner: {winner_name}, "
            f"summary: {latest_match.summary}")



# def get_matches_by_tournament(tournament_name=None):
#     if tournament_name is None:
#         return "No matches found."
#
#     matches = Match.objects \
#         .filter(tournament__name__exact=tournament_name) \
#         .order_by('-date_played')
#
#     if not matches:
#         return "No matches found."
#
#     match_info = []
#     [match_info.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {match.winner.full_name if match.winner else 'TBA'}") for match in matches]
#
#     return '\n'.join(match_info)
#
def get_matches_by_tournament(tournament_name=None):
    if not tournament_name:
        return "No matches found."

    matches = Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')

    if not matches.exists():
        return "No matches found."

    return '\n'.join(
        f"Match played on: {match.date_played}, score: {match.score}, winner: {match.winner.full_name if match.winner else 'TBA'}"
        for match in matches
    )
