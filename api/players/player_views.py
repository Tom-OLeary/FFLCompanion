from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.api_util import split_and_strip, get_queryset_filters
from api.players.player_serializers import PlayerRequestSerializer, PlayerSerializer
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
