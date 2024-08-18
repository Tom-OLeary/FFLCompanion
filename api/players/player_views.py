import operator

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from functools import reduce

from api.api_util import string_to_list, get_queryset_filters, BaseAPIView
from api.players.player_serializers import PlayerRequestSerializer, PlayerSerializer, PlayerSearchSerializer
from ffl_companion.api_models.player import NFLPlayer, Player


class ProjectionListView(BaseAPIView):
    schema_keys = list(PlayerRequestSerializer.__dict__["_declared_fields"].keys())
    model = NFLPlayer

    @extend_schema(
        parameters=[OpenApiParameter(name=k, location="query", type=str) for k in schema_keys],
        responses={"200": PlayerSerializer(many=True)},
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PlayerRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        filter_fields = {
            "stat_type": serializer.validated_data.get("stat_type"),
            "position__in": string_to_list(serializer.validated_data.get("positions")),
            "team__in": string_to_list(serializer.validated_data.get("teams")),
            "pass_yards__gte": serializer.validated_data.get("min_pass_yards"),
            "rush_yards__gte": serializer.validated_data.get("min_rush_yards"),
            "pass_attempts__gte": serializer.validated_data.get("min_pass_attempts"),
            "rush_attempts__gte": serializer.validated_data.get("min_rush_attempts"),
            "targets__gte": serializer.validated_data.get("min_targets"),
            "receptions__gte": serializer.validated_data.get("min_receptions"),
            "receiving_yards__gte": serializer.validated_data.get("min_receiving_yards"),
            "season_start_year": serializer.validated_data.get("season_start_year"),
            "is_available": serializer.validated_data.get("is_available"),
            "fantasy_team__id__in": string_to_list(serializer.validated_data.get("fantasy_team_ids")),
            "fantasy_team__team_name__in": string_to_list(serializer.validated_data.get("fantasy_team_names")),
        }
        players = self.get_queryset().filter(**get_queryset_filters(filter_fields))
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerDetailView(BaseAPIView):
    queryset = NFLPlayer.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "player_id"

    @extend_schema(
        parameters=[OpenApiParameter(name="player_id", location="path", type=str)],
        responses={"200": PlayerSerializer},
    )
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        player = self.get_object()
        return Response(PlayerSerializer(player).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PlayerSerializer,
        parameters=[OpenApiParameter(name="player_id", location="path", type=str)],
        responses={"200": PlayerSerializer},
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        player = self.get_object()
        serializer = PlayerSerializer(player, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerSearchView(BaseAPIView):
    model = Player

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PlayerSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qbs, rbs, wrs, tes, defenses = serializer.validated_data.values()
        names, teams = [], []
        for players in [qbs, rbs, wrs, tes, defenses]:
            for p in players:
                *name, team = p.split(" ")
                names.extend(name)
                teams.append(team.upper())

        results = Player.objects.filter(
            reduce(operator.and_, (Q(name__contains=name) for name in names)),
            nfl_teams__abbreviation__in=teams
        )
        if not results:
            return Response([], status=status.HTTP_200_OK)

        serializer = PlayerSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
