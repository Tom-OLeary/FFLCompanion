from collections import defaultdict
from dataclasses import dataclass, fields

from django.db import models

from ffl_companion.api_models.league_settings import LeagueSettings, LeagueScoring
from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.api_models.player import Player


@dataclass
class StatTotals:
    pass_yds: int = 0
    pass_td: int = 0
    interceptions: int = 0
    receiving_yards: int = 0
    receiving_td: int = 0
    receptions: int = 0
    rush_yds: int = 0
    rush_td: int = 0

    def __iadd__(self, other):
        for f in fields(self):
            _updated = getattr(self, f.name) + getattr(other, f.name)
            setattr(self, f.name, _updated)

        return self


class Trade(models.Model):
    class Meta:
        db_table = "trades"

    # players are considered received, and will have been traded to their current owner
    season_year = models.IntegerField(default=0)
    owner_one = models.ForeignKey(TeamOwner, on_delete=models.CASCADE, related_name="owner_one_trades", null=True)
    owner_two = models.ForeignKey(TeamOwner, on_delete=models.CASCADE, related_name="owner_two_trades", null=True)
    owner_one_received = models.ManyToManyField(Player, related_name="owner_one_received")
    owner_two_received = models.ManyToManyField(Player, related_name="owner_two_received")
    league = models.ForeignKey(LeagueSettings, on_delete=models.CASCADE, related_name="trades")
    trade_date = models.DateField(null=True)

    def get_trade_comparison(self):
        # TODO currently does not support players traded multiple times
        # logic assumes players traded once
        owner_one_received = self.owner_one_received.all()
        owner_two_received = self.owner_two_received.all()
        owner_one_players, owner_two_players = [], []

        results = defaultdict(StatTotals)
        for player in owner_one_received:
            player_stats = player.season_totals(year=self.season_year, fields=LeagueScoring.ALL_FIELDS, trade_date=self.trade_date)[0]
            player_stats.pop("player_id")
            results[self.owner_one.name] += StatTotals(**player_stats)
            owner_one_players.append(player.name)

        for player in owner_two_received:
            player_stats = player.season_totals(year=self.season_year, fields=LeagueScoring.ALL_FIELDS, trade_date=self.trade_date)[0]
            player_stats.pop("player_id")
            results[self.owner_two.name] += StatTotals(**player_stats)
            owner_two_players.append(player.name)

        scoring = self.league.scoring.all()
        final_results = {k: v.__dict__ for k, v in results.items()}
        for key, stats in final_results.items():
            total_points = 0
            for score in scoring:
                stat_name = score.stat_name
                total_points += stats[stat_name] * score.point_value

            final_results[key]["total_points"] = round(total_points, 2)

        final_results[self.owner_one.name]["players_received"] = owner_one_players
        final_results[self.owner_two.name]["players_received"] = owner_two_players
        return final_results
