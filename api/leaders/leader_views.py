from dataclasses import dataclass

import pandas as pd
from django.db.models import F
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.leaders.leader_serializers import LeagueLeadersSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


@dataclass
class LeaderBoard:
    stats: pd.DataFrame

    def __post_init__(self):
        pass

    @property
    def max_points(self):
        _idx = self.stats.groupby("team_owner_id")["total_points"].transform("max") == self.stats["total_points"]
        return self.stats[_idx]

    @property
    def max_wins(self):
        _idx = self.stats.groupby("team_owner_id")["wins"].transform("max") == self.stats["wins"]
        return self.stats[_idx]


class LeagueLeadersView(GenericAPIView):
    CATEGORY_MAP = {
        "titles_sum": ("Total", "Titles"),
        "points_yr": ("Avg", "Points"),
        "wins_yr": ("Avg", "Wins"),
        "total_points": ("Max", "Points"),
        "wins": ("Max", "Wins"),
        "ppg_yr": ("Avg", "PPG"),
        "playoff_appearances": ("Total", "Playoffs"),
        "finals_appearances": ("Total", "Finals"),
        "playoff_rate": ("Rate", "Playoffs"),
    }

    OPERATION_MAP = {
        "titles_sum": ("won_finals", "sum"),
        "playoff_appearances": ("made_playoffs", "sum"),
        "finals_appearances": ("made_finals", "sum"),
        "points_yr": ("total_points", "mean"),
        "wins_yr": ("wins", "mean"),
        "ppg_yr": ("ppg", "mean"),
        "playoff_rate": ("made_playoffs", "mean"),
    }

    QUERY_VALUES = [
        "team_owner_id",
        "wins",
        "total_points",
        "ppg",
        "net_rating",
        "won_finals",
        "made_playoffs",
        "made_finals",
        "season_start_year",
        "team_name",
        "name",
        "is_active",
        "image",
    ]

    def _generate_count(self, rank_df: pd.DataFrame, key: str):
        group_key, operation = self.OPERATION_MAP[key]
        rank_df[key] = rank_df.groupby("team_owner_id")[group_key].transform(operation).round(2)
        rank_df.sort_values(by=[key, "team_owner_id", "season_start_year"], inplace=True, ascending=False)
        return rank_df

    def _generate_max_total(self, df: pd.DataFrame, key: str):
        _idx = df.groupby("team_owner_id")[key].transform("max") == df[key]
        return df[_idx].sort_values(by=[key, "years_count"], ascending=False).round(2)

    def _generate_rank(self, df: pd.DataFrame, key: str, func: str):
        if df.empty:
            return []

        rank_df = df.copy()
        rank_df["category_type"], rank_df["category"] = self.CATEGORY_MAP[key]
        rank_df = getattr(self, func)(rank_df, key).drop_duplicates(subset=["team_owner_id", key], keep="first").rename(columns={key: "total"})
        return rank_df.to_dict("records")

    # def _generate_rank(self, df: pd.DataFrame, key: str) -> list[dict]:
    #     if df.empty:
    #         return []
    #
    #     rank_df = self._generate_rank()(df, key)
    #     rank_df.rename(columns={key: "total"}, inplace=True)
    #
    #     return rank_df.to_dict("records")

    def get_queryset(self):
        return FantasyTeamStats.objects.select_related("team_owner").annotate(
            name=F("team_owner__name"),
            is_active=F("team_owner__is_active"),
            image=F("team_owner__image")
        ).values(*self.QUERY_VALUES)

    def get(self, request):
        stats = self.get_queryset()
        stats_df = pd.DataFrame(stats)
        stats_df["years_count"] = stats_df.groupby("team_owner_id")["team_owner_id"].transform("count")
        stats_df.fillna(0, inplace=True)

        serializer = LeagueLeadersSerializer(
            dict(
                # -------------- counts/rates
                titles=self._generate_rank(stats_df, "titles_sum", "_generate_count"),
                playoffs=self._generate_rank(stats_df, "playoff_appearances", "_generate_count"),
                finals=self._generate_rank(stats_df, "finals_appearances", "_generate_count"),
                points=self._generate_rank(stats_df, "points_yr", "_generate_count"),
                wins=self._generate_rank(stats_df, "wins_yr", "_generate_count"),
                ppg=self._generate_rank(stats_df, "ppg_yr", "_generate_count"),
                playoff_rate=self._generate_rank(stats_df, "playoff_rate", "_generate_count"),
                # -------------- max totals
                points_max=self._generate_rank(stats_df, "total_points", "_generate_max_total"),
                wins_max=self._generate_rank(stats_df, "wins", "_generate_max_total"),
            )
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
