import pandas as pd
from django.db.models import Sum, Count, Case, When, F, Avg, Max
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.leaders.leader_serializers import ReigningChampsSerializer, LeagueLeadersSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class LeagueLeadersView(GenericAPIView):
    CATEGORY_MAP = {
        "titles_sum": ("Total", "Titles"),
        "points_yr": ("Avg", "Points"),
        "wins_yr": ("Avg", "Wins"),
        "points_max": ("Max", "Points"),
        "wins_max": ("Max", "Wins"),
        "ppg_yr": ("Avg", "PPG"),
        "playoff_appearances": ("Total", "Playoffs"),
        "finals_appearances": ("Total", "Finals"),
        "playoff_rate": ("Rate", "Playoffs"),
    }

    RATE_CALC = {
        "playoff_rate": "playoff_appearances"
    }

    def _generate_rank(self, df: pd.DataFrame, key: str) -> list[dict]:
        if df.empty:
            return []

        df.fillna(0, inplace=True)
        if key in self.RATE_CALC:
            df[key] = df[self.RATE_CALC[key]] / df["years_count"]

        df["category_type"], df["category"] = self.CATEGORY_MAP[key]
        sorted_data = df.sort_values(by=[key, "years_count"], ascending=False).round(2)
        sorted_data.rename(columns={key: "total"}, inplace=True)

        return sorted_data.to_dict("records")

    def get_queryset(self):
        return FantasyTeamStats.objects.values("team_owner__id").annotate(
            titles_sum=Count(Case(When(won_finals=True, then=1))),
            points_yr=Avg("total_points"),
            wins_yr=Avg("wins"),
            points_max=Max("total_points"),
            wins_max=Max("wins"),
            ppg_yr=Avg("ppg"),
            playoff_appearances=Count(Case(When(made_playoffs=True, then=1))),
            finals_appearances=Count(Case(When(made_finals=True, then=1))),
            # ---------------------------------
            years_count=Count("team_owner__id"),
            name=F("team_owner__name"),
            is_active=F("team_owner__is_active"),
            team_name=Max("team_name"),
            image=Max("team_owner__image"),
        )

    def get(self, request):
        stats = self.get_queryset()
        stats_df = pd.DataFrame(stats)

        serializer = LeagueLeadersSerializer(
            dict(
                titles=self._generate_rank(stats_df, "titles_sum"),
                points=self._generate_rank(stats_df, "points_yr"),
                wins=self._generate_rank(stats_df, "wins_yr"),
                points_max=self._generate_rank(stats_df, "points_max"),
                wins_max=self._generate_rank(stats_df, "wins_max"),
                ppg=self._generate_rank(stats_df, "ppg_yr"),
                playoffs=self._generate_rank(stats_df, "playoff_appearances"),
                finals=self._generate_rank(stats_df, "finals_appearances"),
                playoff_rate=self._generate_rank(stats_df, "playoff_rate"),
            )
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
