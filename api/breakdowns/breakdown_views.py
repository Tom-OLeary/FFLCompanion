from dataclasses import dataclass

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

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
    queryset = LeagueSettings.objects.all()

    def get(self, request):
        # using self.get_queryset would ignore App config filter
        leagues = LeagueSettings.objects.order_by("-setting_year")
        owners = TeamOwner.objects.all()
        if league_name := request.GET.get("name"):
            leagues = leagues.filter(name=league_name)
            owners = owners.filter(name=league_name)

        return Response(LeagueBreakdown(leagues=leagues, owners=owners).data, status=status.HTTP_200_OK)
