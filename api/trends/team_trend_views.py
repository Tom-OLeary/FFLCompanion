from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.trends.trends_serializers import TeamTrendSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class TeamTrendView(BaseAPIView):
    model = FantasyTeamStats

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        stats = self.get_queryset().select_related("owner").order_by("season_start_year")
        if not stats:
            return Response([], status=status.HTTP_200_OK)

        years = set()
        teams = OrderedDict()

        def set_stats(rows):
            for stat in rows:
                owner_name = stat.owner.name
                if owner_name not in teams:
                    teams[owner_name] = []

                teams[owner_name].append(stat)
                years.add(str(stat.season_start_year))

        set_stats(stats.filter(owner__is_active=True))
        set_stats(stats.filter(owner__is_active=False))  # displays inactive teams last

        # columns for selection bar
        columns = [
            "total_points",
            "wins",
            "losses",
            "draws",
            "total_points_against",
            "ppg",
            "pag",
            "net_rating",
            "final_season_standing",
            "made_playoffs",
            "made_finals",
            "won_finals",
        ]
        results = {
            "data": [{"team_owner": k, "stats": v, "years": years} for k, v in teams.items()],
            "years": sorted(list(years)),
            "columns": columns,
        }
        return Response(TeamTrendSerializer(results).data, status=status.HTTP_200_OK)
