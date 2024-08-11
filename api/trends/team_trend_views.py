from collections import defaultdict

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

        stats = self.get_queryset().order_by("season_start_year")
        if not stats:
            return Response([], status=status.HTTP_200_OK)

        years = set()
        teams = defaultdict(list)
        for stat in stats:
            teams[stat.team_owner.name].append(stat)
            years.add(str(stat.season_start_year))

        results = {
            "data": [{"team_owner": k, "stats": v, "years": years} for k, v in teams.items()],
            "years": sorted(list(years)),
        }
        return Response(TeamTrendSerializer(results).data, status=status.HTTP_200_OK)
