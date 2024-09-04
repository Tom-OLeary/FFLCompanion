import pandas as pd
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.decorators import require_token
from api.leaders.categories import (
    Rank,
    TotalTitles,
    AvgPoints,
    AvgWins,
    AvgPPG,
    TotalPlayoffs,
    TotalFinals,
    PlayoffRate,
    MaxPoints,
    MaxWins
)
from api.leaders.leader_serializers import LeagueLeaderSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class LeagueLeadersView(BaseAPIView):
    model = FantasyTeamStats

    QUERY_VALUES = [
        "owner_id",
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

    CATEGORIES = (
        TotalTitles,
        AvgPoints,
        AvgWins,
        AvgPPG,
        TotalPlayoffs,
        TotalFinals,
        PlayoffRate,
        MaxPoints,
        MaxWins,
    )

    @require_token
    def get(self, request):
        stats = self.get_queryset().select_related("owner").annotate(
            name=F("owner__name"),
            is_active=F("owner__is_active"),
            image=F("owner__image")
        ).values(*self.QUERY_VALUES)
        if not stats:
            return Response([], status=status.HTTP_200_OK)

        generator = Rank(pd.DataFrame(stats))
        for category in self.CATEGORIES:
            generator.register(category)

        serializer = LeagueLeaderSerializer(generator.run())
        return Response(serializer.data, status=status.HTTP_200_OK)
