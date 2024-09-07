from django.db.models import QuerySet, Max

from ffl_companion.api_models.player import PlayerStatsWeekly, Player
from ffl_companion.constants import QueryAgg


class PlayerStatsGenerator:
    _STATS = [
        *PlayerStatsWeekly.PASSING,
        *PlayerStatsWeekly.RECEIVING,
        *PlayerStatsWeekly.RUSHING,
    ]

    _AGG: QueryAgg = None
    _GROUP: tuple = None

    def __init__(self, players: QuerySet[Player]):
        if not all([self._AGG, self._GROUP]):
            raise ValueError("Both _AGG & _GROUP attributes must be set")

        self._players = players

    def generate(self) -> QuerySet:
        agg = {f"{k}": self._AGG(f"stats_weekly__{k}") for k in self._STATS}
        return self._players.select_related("stats_weekly").values(*self._GROUP).annotate(
            **agg,
            **{k.split("__")[-1]: Max(k) for k in self._GROUP},
        )


class GenerateTotal(PlayerStatsGenerator):
    _AGG = QueryAgg.SUM
    _GROUP = ("stats_weekly__player_id",)


class GenerateAdvanced(PlayerStatsGenerator):
    pass


class GenerateDailySplits(PlayerStatsGenerator):
    _AGG = QueryAgg.AVG
    _GROUP = ("stats_weekly__player_id", "stats_weekly__day_of_week")

