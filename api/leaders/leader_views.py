import pandas as pd
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.leaders.leader_serializers import LeagueLeadersSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class LeagueLeadersView(BaseAPIView):
    model = FantasyTeamStats

    CATEGORY_MAP = {
        "titles_sum": ("Total", "Titles"),
        "points_yr": ("Avg", "Points"),
        "wins_yr": ("Avg", "Wins"),
        "total_points": ("Total", "Points"),
        "wins": ("Total", "Wins"),
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

    def _generate_leader(self, rank_df: pd.DataFrame, key: str):
        group_key, operation = self.OPERATION_MAP[key]
        rank_df[key] = rank_df.groupby("team_owner_id")[group_key].transform(operation).round(2)
        rank_df.sort_values(by=[key, "team_owner_id", "season_start_year"], inplace=True, ascending=False)
        return rank_df

    @staticmethod
    def _generate_max_total(df: pd.DataFrame, key: str):
        _idx = df.groupby("team_owner_id")[key].transform("max") == df[key]
        return df[_idx].sort_values(by=[key, "years_count"], ascending=False).round(2)

    def _generate_rank(self, df: pd.DataFrame, key: str, func: str):
        if df.empty:
            return []

        rank_df = df.copy()
        rank_df["category_type"], rank_df["category"] = self.CATEGORY_MAP[key]
        rank_df = getattr(self, func)(rank_df, key).drop_duplicates(subset=["team_owner_id", key], keep="first").rename(columns={key: "total"})
        return rank_df.to_dict("records")

    def get(self, request):
        stats = self.get_queryset().select_related("team_owner").annotate(
            name=F("team_owner__name"),
            is_active=F("team_owner__is_active"),
            image=F("team_owner__image")
        ).values(*self.QUERY_VALUES)

        stats_df = pd.DataFrame(stats)
        stats_df["years_count"] = stats_df.groupby("team_owner_id")["team_owner_id"].transform("count")
        stats_df.fillna(0, inplace=True)

        serializer = LeagueLeadersSerializer(
            dict(
                # -------------- counts/rates
                titles=self._generate_rank(stats_df, "titles_sum", "_generate_leader"),
                playoffs=self._generate_rank(stats_df, "playoff_appearances", "_generate_leader"),
                finals=self._generate_rank(stats_df, "finals_appearances", "_generate_leader"),
                points=self._generate_rank(stats_df, "points_yr", "_generate_leader"),
                wins=self._generate_rank(stats_df, "wins_yr", "_generate_leader"),
                ppg=self._generate_rank(stats_df, "ppg_yr", "_generate_leader"),
                playoff_rate=self._generate_rank(stats_df, "playoff_rate", "_generate_leader"),
                # -------------- max totals, these results rely upon the specific row the data comes from
                points_max=self._generate_rank(stats_df, "total_points", "_generate_max_total"),
                wins_max=self._generate_rank(stats_df, "wins", "_generate_max_total"),
                # net_rating_max=self._generate_rank(stats_df, "net_rating", "_generate_max_total"),
            )
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
