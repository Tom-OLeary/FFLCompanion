from dataclasses import dataclass

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.breakdowns.breakdown_serializers import YearlyStatsSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from owner.models import Owner


@dataclass
class LeagueBreakdown:
    leagues: QuerySet[LeagueSettings]
    owners: QuerySet[Owner]

    @property
    def data(self) -> dict:
        _champions = self.leagues.filter(league_stats__final_season_standing=1).values_list("league_stats__owner__name")
        _most_recent = self.leagues.first()

        return {
            "years_active": self.leagues.count(),
            "active_members": _most_recent.member_count,
            "total_members": self.owners.count(),
            "unique_champions": len(set(c[0] for c in _champions)),
            "prize_pool": _most_recent.prize_pool,
        }


class LeagueBreakdownView(BaseAPIView):
    model = LeagueSettings

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        leagues = self.get_queryset().order_by("-setting_year")
        owners = self.protected_query(Owner)
        if league_name := request.GET.get("name"):
            leagues = leagues.filter(name=league_name)
            owners = owners.filter(league_name=league_name)

        return Response(LeagueBreakdown(leagues=leagues, owners=owners).data, status=status.HTTP_200_OK)


class YearlyStatsView(BaseAPIView):
    model = FantasyTeamStats

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        stats = self.get_queryset()
        serializer = YearlyStatsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
