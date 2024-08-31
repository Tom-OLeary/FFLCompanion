import operator

from django.conf import settings
from django.db.models import Q, QuerySet, Sum, Avg, Max
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from functools import reduce

from api.api_util import string_to_list, get_queryset_filters, BaseAPIView
from api.players.player_serializers import (
    PlayerRequestSerializer,
    PlayerSerializer,
    PlayerSearchSerializer,
    PlayerSearchResponseSerializer, PlayerStatsRequestSerializer, PlayerStatsSplitsResponseSerializer,
)
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import NFLPlayer, Player, PlayerStatsWeekly
from ffl_companion.api_models.roster import Roster


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
        serializer.validated_data.pop("players", None)

        qbs, rbs, wrs, tes, defenses = serializer.validated_data.values()
        names, teams = [], set()

        def add(player):
            *fullname, team = player.split(" ")
            names.append(fullname)
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
            position__in=["QB", "RB", "WR", "TE", "DEF"],
        ).distinct()
        if not results:
            return Response([], status=status.HTTP_200_OK)

        serializer = PlayerSearchResponseSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WaiverView(BaseAPIView):
    model = Player

    def get(self, request):
        """Returns list of all available players for user's current league"""
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        unavailable_players = self.protected_query(Roster).prefetch_related("players").filter(
            roster_year=settings.CURRENT_YEAR
        ).values_list("players__id")

        unavailable_player_ids = [p[0] for p in unavailable_players] if unavailable_players else []
        available_players = self.get_queryset().exclude(id__in=unavailable_player_ids).order_by("id")
        serializer = PlayerSearchResponseSerializer(available_players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerStatsGenerator:
    STATS = [
        *PlayerStatsWeekly.PASSING,
        *PlayerStatsWeekly.RECEIVING,
        *PlayerStatsWeekly.RUSHING,
    ]

    def __init__(self, players: QuerySet[Player], split_type: str):
        self._players = players
        self._split_type = split_type
        self._split_key_map = {
            "total": {
                "agg": [(k, Sum) for k in self.STATS],
                "group_key": ("stats_weekly__player_id",)
            },
            "advanced": [],
            "splits": {
                "agg": [(k, Avg) for k in self.STATS],
                "group_key": ("stats_weekly__player_id", "stats_weekly__day_of_week")
            }
        }

    def generate(self) -> QuerySet:
        key = self._split_key_map[self._split_type]
        agg = {f"{k[0]}": k[1](f"stats_weekly__{k[0]}") for k in key["agg"]}
        return self._players.select_related("stats_weekly").values(*key["group_key"]).annotate(
            **agg,
            **{k.split("__")[-1]: Max(k) for k in key["group_key"]},
        )


class PlayerStatsView(BaseAPIView):
    model = PlayerStatsWeekly

    SERIALIZER_MAP = {
        "total": None,  # TODO
        "advanced": None,  # TODO
        "splits": PlayerStatsSplitsResponseSerializer,
    }

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PlayerStatsRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        split_type = serializer.validated_data.get("split_type") or "total"
        if split_type not in self.SERIALIZER_MAP:
            return Response(f"Split type {split_type} not found", status=status.HTTP_400_BAD_REQUEST)

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

        generator = PlayerStatsGenerator(players=players, split_type=split_type)
        serializer = self.SERIALIZER_MAP[split_type](generator.generate(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
