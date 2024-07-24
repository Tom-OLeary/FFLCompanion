from dataclasses import dataclass

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.api_util import get_queryset_filters, split_and_strip
from api.fantasy_tracker.nfl_serializers import PlayerRequestSerializer, PlayerSerializer, TeamOwnerSerializer
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.api_models.player import NFLPlayer


class PlayerListView(GenericAPIView):
    schema_keys = list(PlayerRequestSerializer.__dict__["_declared_fields"].keys())
    queryset = NFLPlayer.objects.all()

    @extend_schema(
        parameters=[OpenApiParameter(name=k, location="query", type=str) for k in schema_keys],
        responses={"200": PlayerSerializer(many=True)},
    )
    def get(self, request):
        serializer = PlayerRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        filter_fields = {
            "stat_type": serializer.validated_data.get("stat_type"),
            "position__in": split_and_strip(serializer.validated_data.get("positions")),
            "team__in": split_and_strip(serializer.validated_data.get("teams")),
            "pass_yards__gte": serializer.validated_data.get("min_pass_yards"),
            "rush_yards__gte": serializer.validated_data.get("min_rush_yards"),
            "pass_attempts__gte": serializer.validated_data.get("min_pass_attempts"),
            "rush_attempts__gte": serializer.validated_data.get("min_rush_attempts"),
            "targets__gte": serializer.validated_data.get("min_targets"),
            "receptions__gte": serializer.validated_data.get("min_receptions"),
            "receiving_yards__gte": serializer.validated_data.get("min_receiving_yards"),
            "season_start_year": serializer.validated_data.get("season_start_year"),
            "is_available": serializer.validated_data.get("is_available"),
            "fantasy_team__id__in": split_and_strip(serializer.validated_data.get("fantasy_team_ids")),
            "fantasy_team__team_name__in": split_and_strip(serializer.validated_data.get("fantasy_team_names")),
        }
        players = self.get_queryset().filter(**get_queryset_filters(filter_fields))
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerDetailView(GenericAPIView):
    queryset = NFLPlayer.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "player_id"

    @extend_schema(
        parameters=[OpenApiParameter(name="player_id", location="path", type=str)],
        responses={"200": PlayerSerializer},
    )
    def get(self, request, *args, **kwargs):
        player = self.get_object()
        return Response(PlayerSerializer(player).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PlayerSerializer,
        parameters=[OpenApiParameter(name="player_id", location="path", type=str)],
        responses={"200": PlayerSerializer},
    )
    def post(self, request, *args, **kwargs):
        player = self.get_object()
        serializer = PlayerSerializer(player, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamOwnerListView(GenericAPIView):
    queryset = TeamOwner.objects.all()

    def get(self, request):
        owners = self.get_queryset()
        return Response(TeamOwnerSerializer(owners, many=True).data, status=status.HTTP_200_OK)


class TeamOwnerDetailView(GenericAPIView):
    queryset = TeamOwner.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "owner_id"

    @extend_schema(
        parameters=[OpenApiParameter(name="owner_id", location="path", type=str)],
        responses={"200": TeamOwnerSerializer},
    )
    def get(self, request, *args, **kwargs):
        owner = self.get_object()
        return Response(TeamOwnerSerializer(owner).data, status=status.HTTP_200_OK)


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
            "active_members": self.owners.filter(is_active=True).count(),
            "total_members": _most_recent.member_count,
            "unique_champions": len(set(c[0] for c in _champions)),
            "prize_pool": _most_recent.prize_pool,
        }


class LeagueBreakdownView(GenericAPIView):
    queryset = LeagueSettings.objects.all()

    def get(self, request):
        leagues = self.get_queryset().order_by("-setting_year")
        owners = TeamOwner.objects.all()
        if league_name := request.GET.get("name"):
            leagues = leagues.filter(name=league_name)
            owners = owners.filter(name=league_name)

        return Response(LeagueBreakdown(leagues=leagues, owners=owners).data, status=status.HTTP_200_OK)
