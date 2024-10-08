from dataclasses import dataclass, fields

from django.db import models
from django.db.models import QuerySet

from ffl_companion.api_models.base import BaseModel, BaseModelManager
from ffl_companion.api_models.league_settings import LeagueSettings, LeagueScoring
from ffl_companion.api_models.player import Player
from owner.models import Owner


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


class TradeModelManager(BaseModelManager):
    pass


class Trade(BaseModel):
    class Meta:
        db_table = "trades"

    season_year = models.IntegerField(default=0)
    first_owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="first_owner_trades", null=True)
    second_owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="second_owner_trades", null=True)
    owner_one_received = models.ManyToManyField(Player, related_name="owner_one_received")
    owner_two_received = models.ManyToManyField(Player, related_name="owner_two_received")
    league = models.ForeignKey(LeagueSettings, on_delete=models.CASCADE, related_name="trades")
    trade_date = models.DateField(null=True)

    objects = TradeModelManager()

    def get_trade_comparison(self) -> dict:
        # TODO currently does not support players traded multiple times
        # logic assumes players traded once

        results: dict[str, any] = {}
        results[self.first_owner.name], first_owner_players = self._get_owner_totals(self.owner_one_received.all())
        results[self.second_owner.name], second_owner_players = self._get_owner_totals(self.owner_two_received.all())

        scoring = self.league.scoring.all()
        for key, stats in results.items():
            results[key]["total_points"] = round(sum(stats[score.stat_name] * score.point_value for score in scoring), 2)

        results[self.first_owner.name]["players_received"] = first_owner_players
        results[self.first_owner.name]["team_name"] = self.first_owner.stats.get(season_start_year=self.season_year).team_name

        results[self.second_owner.name]["players_received"] = second_owner_players
        results[self.second_owner.name]["team_name"] = self.second_owner.stats.get(season_start_year=self.season_year).team_name
        results["winner"] = None

        first_owner_total = results[self.first_owner.name]["total_points"]
        second_owner_total = results[self.second_owner.name]["total_points"]
        if abs(first_owner_total - second_owner_total) > 30:
            if first_owner_total > second_owner_total:
                results["winner"] = self.first_owner.name
            else:
                results["winner"] = self.second_owner.name

        final_results = {
            "winner": results["winner"],
            "trade_date": self.trade_date,
            "details": [
                {
                    "team_owner": self.first_owner.name,
                    **results[self.first_owner.name],
                },
                {
                    "team_owner": self.second_owner.name,
                    **results[self.second_owner.name],
                },
            ]
        }
        return final_results

    def _get_owner_totals(self, players: QuerySet) -> tuple:
        totals = StatTotals()
        players_received = []
        for player in players:
            player_stats = player.season_totals(
                year=self.season_year,
                fields=LeagueScoring.ALL_FIELDS,
                trade_date=self.trade_date,
            )[0]
            player_stats.pop("player_id")
            totals += StatTotals(**player_stats)
            players_received.append(player.name)

        return totals.__dict__, players_received

    def __getitem__(self, owner: Owner):
        _owner = "owner_one"
        if owner == self.second_owner:
            _owner = "owner_two"

        return {
            "season_year": self.season_year,
            "owner_name": owner.name,
            "players_received": getattr(self, f"{_owner}_received").all(),
            "league": self.league,
            "trade_date": self.trade_date,
        }
