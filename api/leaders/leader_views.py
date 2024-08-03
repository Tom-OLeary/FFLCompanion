import json

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
        "points_yr": ("Total", "Points"),
        "wins_yr": ("Total", "Wins"),
    }

    def _generate_rank(self, df: pd.DataFrame, key: str) -> list[dict]:
        if df.empty:
            return []

        df["category_type"], df["category"] = self.CATEGORY_MAP[key]
        sorted_data = df.sort_values(by=[key, "years_count"], ascending=False)
        sorted_data.rename(columns={key: "total"}, inplace=True)

        return sorted_data.to_dict("records")

    def get_queryset(self):
        return FantasyTeamStats.objects.values("team_owner__id").annotate(
            years_count=Count("team_owner__id"),
            titles_sum=Count(Case(When(won_finals=True, then=1))),
            name=F("team_owner__name"),
            is_active=F("team_owner__is_active"),
            team_name=Max("team_name"),
            points_yr=Avg("total_points"),
            wins_yr=Avg("wins"),
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
            )
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
