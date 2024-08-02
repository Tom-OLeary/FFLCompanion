import pandas as pd
from django.db.models import Sum, Count, Case, When, F
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.leaders.leader_serializers import ReigningChampsSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class LeagueLeadersView(GenericAPIView):
    queryset = FantasyTeamStats.objects.all()

    @staticmethod
    def _get_highest_total(df: pd.DataFrame, key: str) -> pd.DataFrame:
        highest_total = df[df[key] == df[key].max()]
        if int(highest_total.count()["team_owner__id"]) > 1:
            highest_total = highest_total.sort_values(by="years_count", ascending=False)
        return highest_total

    def get(self, request):
        # TODO test config filter
        reigning_champs = FantasyTeamStats.objects.filter(won_finals=True, is_current_season=False).order_by("-season_start_year")
        stats = self.get_queryset().values("team_owner__id").annotate(
            points_sum=Sum("total_points"),
            years_count=Count("team_owner__id"),
            titles_sum=Count(Case(When(won_finals=True, then=1))),
            wins_sum=Sum("wins"),
            owner_name=F("team_owner__name"),
            is_active=F("team_owner__is_active"),
            # points_average=Avg("total_points"),
        )
        stats_df = pd.DataFrame(stats)
        stats_df["wins_yr"] = round(stats_df["wins_sum"] / stats_df["years_count"], 2)
        stats_df["points_yr"] = round(stats_df["points_sum"] / stats_df["years_count"], 2)

        most_titles = self._get_highest_total(stats_df, "titles_sum")
        most_points_py = self._get_highest_total(stats_df, "points_yr")
        most_wins_py = self._get_highest_total(stats_df, "wins_yr")

        results = {
            "most_titles_owner": most_titles.iloc[0].owner_name,
            "most_titles_count": int(most_titles.iloc[0].titles_sum),
            "total_points_py_owner": most_points_py.iloc[0].owner_name,
            "total_points_py": float(most_points_py.iloc[0].points_yr),  # py = per year
            "total_points_yrs_in_league": int(most_points_py.iloc[0].years_count),
            "total_wins_py_owner": most_wins_py.iloc[0].owner_name,
            "total_wins_py": float(most_wins_py.iloc[0].wins_yr),
            "total_wins_yrs_in_league": int(most_wins_py.iloc[0].years_count),
            "reigning_champs": ReigningChampsSerializer(reigning_champs, many=True).data,
            "full_results": stats_df.to_dict("records"),
        }
        return Response(results, status=status.HTTP_200_OK)
