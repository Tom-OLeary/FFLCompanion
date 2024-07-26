from django.db import models

from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.api_models.player import Player


class Trade(models.Model):
    class Meta:
        db_table = "trades"

    # players are considered received, and will have been traded to their current owner
    season_year = models.IntegerField(default=0)
    league = models.ForeignKey(LeagueSettings, on_delete=models.CASCADE, related_name="trades")
    owners = models.ManyToManyField(TeamOwner, related_name="owner_trades")
    players = models.ManyToManyField(Player, related_name="player_trades")

    

