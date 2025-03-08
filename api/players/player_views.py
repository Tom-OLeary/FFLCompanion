import operator

from django.conf import settings
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from functools import reduce

from api.api_util import string_to_list, get_queryset_filters, BaseAPIView
from api.decorators import require_token
from api.players.player_serializers import (
    PlayerRequestSerializer,
    PlayerSerializer,
    PlayerSearchSerializer,
    PlayerSearchResponseSerializer, PlayerStatsRequestSerializer, PlayerStatsSplitsResponseSerializer,
)
from api.players.util import GenerateTotal, GenerateDailySplits
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import NFLPlayer, Player, PlayerStatsWeekly
from ffl_companion.api_models.roster import Roster
from ffl_companion.constants import PLAYER_STATS as PS


class ProjectionListView(BaseAPIView):
    schema_keys = list(PlayerRequestSerializer.__dict__["_declared_fields"].keys())
    model = NFLPlayer

    @require_token
    @extend_schema(
        parameters=[OpenApiParameter(name=k, location="query", type=str) for k in schema_keys],
        responses={"200": PlayerSerializer(many=True)},
    )
    def get(self, request):
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

    @require_token
    @extend_schema(
        parameters=[OpenApiParameter(name="player_id", location="path", type=str)],
        responses={"200": PlayerSerializer},
    )
    def get(self, request, *args, **kwargs):
        player = self.get_object()
        return Response(PlayerSerializer(player).data, status=status.HTTP_200_OK)

    @require_token
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


class PlayerSearchView(BaseAPIView):
    model = Player

    @require_token
    def post(self, request):
        serializer = PlayerSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("players", None)

        qbs, rbs, wrs, tes, defenses = serializer.validated_data.values()
        names, teams = [], set()

        def add(player):
            *fullname, team = player.split(" ")
            if fullname and len(fullname) == 2:
                names.append(fullname)

            if team:
                teams.add(team.upper())

        for players in [qbs, rbs, wrs, tes]:
            for p in players:
                add(p)

        for defense in defenses:
            if len(defense) > 3:
                # is full name, not abbreviation
                add(defense)
            else:
                defense = defense.upper()
                teams.add(defense)

                try:
                    name = NFLTeam.objects.filter(abbreviation=defense).first().name
                    name = name.split(" ")
                    names.append((name[0], name[1]))
                except (AttributeError, IndexError):
                    continue

        if not names:
            return Response([], status=status.HTTP_200_OK)

        results = Player.objects.filter(
            reduce(operator.or_, (Q(name__contains=name[0]) & Q(name__contains=name[1]) for name in names)),
            nfl_teams__abbreviation__in=teams,
            position__in=PS.positions(),
        ).distinct()
        if not results:
            return Response([], status=status.HTTP_200_OK)

        serializer = PlayerSearchResponseSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WaiverView(BaseAPIView):
    model = Player

    @require_token
    def get(self, request):
        """Returns list of all available players for user's current league"""
        unavailable_players = self.protected_query(Roster).prefetch_related("players").filter(
            roster_year=settings.CURRENT_YEAR
        ).values_list("players__id")

        unavailable_player_ids = [p[0] for p in unavailable_players] if unavailable_players else []
        available_players = self.get_queryset().exclude(id__in=unavailable_player_ids).order_by("id")
        serializer = PlayerSearchResponseSerializer(available_players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerStatsView(BaseAPIView):
    model = PlayerStatsWeekly

    SPLIT_TYPE_MAP: dict[tuple] = {
        "total": (GenerateTotal, None),  # TODO
        "advanced": (None, None),  # TODO
        "splits": (GenerateDailySplits, PlayerStatsSplitsResponseSerializer),
    }

    @require_token
    def get(self, request):
        serializer = PlayerStatsRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        split_type = serializer.validated_data.get("split_type") or "total"
        if split_type not in self.SPLIT_TYPE_MAP:
            return Response(f"Split type {split_type} not found. Choices are {self.SPLIT_TYPE_MAP.keys()}", status=status.HTTP_400_BAD_REQUEST)

        # roster_id takes priority over player_ids if both are included
        if roster_id := serializer.validated_data.get("roster_id"):
            try:
                roster = self.protected_query(Roster).get(id=roster_id)
            except Roster.DoesNotExist:
                return Response(f"Roster {roster_id} not found", status=status.HTTP_404_NOT_FOUND)

            players = roster.players.all()
        else:
            player_ids = string_to_list(serializer.validated_data.get("player_ids", []))
            players = Player.objects.filter(id__in=player_ids)

        generator, serializer = self.SPLIT_TYPE_MAP[split_type]
        generator = generator(players=players)
        serializer = serializer(generator.generate(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
