from django.db.models import manager, Count


class TennisPlayerManager(manager.Manager):

    def get_tennis_players_by_wins_count(self):

        return (self.annotate(num_wins=Count('matches_winner'))
                .order_by('-num_wins', 'full_name'))


