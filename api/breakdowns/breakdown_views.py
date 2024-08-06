from dataclasses import dataclass

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.breakdowns.breakdown_serializers import YearlyStatsSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.owner import TeamOwner


@dataclass
class LeagueBreakdown:
    leagues: QuerySet[LeagueSettings]
    owners: QuerySet[TeamOwner]

    @property
    def data(self) -> dict:
        _champions = self.leagues.filter(league_stats__final_season_standing=1).values_list("league_stats__team_owner__name")
        _most_recent = self.leagues.first()

        return {
            "years_active": self.leagues.count(),
            "active_members": _most_recent.member_count,
            "total_members": self.owners.count(),
            "unique_champions": len(set(c[0] for c in _champions)),
            "prize_pool": _most_recent.prize_pool,
        }


class LeagueBreakdownView(GenericAPIView):
    def get_queryset(self):
        return LeagueSettings.objects.all()

    def get(self, request):
        leagues = self.get_queryset().order_by("-setting_year")
        owners = TeamOwner.objects.all()
        if league_name := request.GET.get("name"):
            leagues = leagues.filter(name=league_name)
            owners = owners.filter(name=league_name)

        return Response(LeagueBreakdown(leagues=leagues, owners=owners).data, status=status.HTTP_200_OK)


class YearlyStatsView(GenericAPIView):
    def get_queryset(self):
        return FantasyTeamStats.objects.all()

    def get(self, request):
        stats = self.get_queryset()
        serializer = YearlyStatsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
