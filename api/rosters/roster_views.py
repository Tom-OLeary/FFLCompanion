from collections import defaultdict
from typing import Union

from django.conf import settings
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView, string_to_list
from api.decorators import require_token
from api.rosters.roster_serializers import (
    RosterImportSerializer,
    RosterSerializer,
    LatestRosterRequestSerializer,
    RosterUpdateRequestSerializer,
)
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.player import Player
from ffl_companion.api_models.roster import Roster


class RosterView(BaseAPIView):
    model = Player

    @require_token
    def get(self, request):
        rosters = self.protected_query(Roster)
        if not rosters:
            return Response([], status.HTTP_200_OK)

        serializer = RosterSerializer(rosters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @require_token
    def post(self, request):
        """Create new Roster for current year"""
        serializer = RosterImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        player_ids = string_to_list(serializer.validated_data["player_ids"])
        players = self.get_queryset().filter(id__in=player_ids)
        if players.count() != len(player_ids):
            return Response("One or more players not found", status.HTTP_400_BAD_REQUEST)

        roster = self.request.user.latest_roster
        if roster and roster.roster_year == settings.CURRENT_YEAR:
            return Response("Roster already exists for current season", status.HTTP_400_BAD_REQUEST)

        try:
            league = self.protected_query(LeagueSettings).get(setting_year=settings.CURRENT_YEAR)
        except LeagueSettings.DoesNotExist:
            return Response("Could not find league for given year", status.HTTP_400_BAD_REQUEST)

        roster = Roster.objects.create(
            dataset=self.request.user.dataset,
            roster_year=settings.CURRENT_YEAR,
            league=league,
            owner=self.request.user,
        )
        roster.players.set(players)

        return Response("ok", status=status.HTTP_200_OK)


class LatestRosterView(BaseAPIView):
    model = Roster

    @require_token
    def get(self, request, *args, **kwargs):
        serializer = LatestRosterRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("latest"):
            roster = self.request.user.latest_roster
            if not roster:
                return Response({}, status.HTTP_200_OK)
        else:
            roster_id = serializer.validated_data.get("roster_id")
            if not roster_id:
                return Response("Roster ID required", status.HTTP_400_BAD_REQUEST)

            try:
                roster = self.protected_query(Roster).get(id=roster_id)
            except Roster.DoesNotExist:
                return Response("Roster not found", status.HTTP_404_NOT_FOUND)

        serializer = RosterSerializer(roster)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RosterDetailView(BaseAPIView):
    model = Roster
    lookup_field = "id"
    lookup_url_kwarg = "roster_id"

    @require_token
    def post(self, request, *args, **kwargs):
        serializer = RosterUpdateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        roster = self.get_object()
        player_add_ids = string_to_list(serializer.validated_data.get("player_add_ids", []))
        player_drop_ids = string_to_list(serializer.validated_data.get("player_drop_ids", []))

        # safety measure to avoid duplicate rosters for single player
        if player_add_ids:
            players = Player.objects.filter(id__in=player_add_ids)
            for player in players:
                if not player.is_available(self.request.user.dataset):
                    return Response("One or more players not available", status.HTTP_400_BAD_REQUEST)

        player_ids = set([p.id for p in roster.players.all()] + [int(p) for p in player_add_ids]) - set(int(p) for p in player_drop_ids)
        roster.players.set(player_ids)
        return Response("ok", status=status.HTTP_200_OK)

    @require_token
    def delete(self, request, *args, **kwargs):
        roster = self.get_object()
        if roster.owner != self.request.user:
            return Response(f"Roster cannot be deleted by this owner", status.HTTP_403_FORBIDDEN)

        roster.delete()
        return Response("deleted", status=status.HTTP_200_OK)


class RosterBreakdownView(BaseAPIView):
    model = Roster
    lookup_field = "id"
    lookup_url_kwarg = "roster_id"

    @require_token
    def get(self, request, *args, **kwargs):
        roster = self.get_object()
        league_rosters = self.protected_query(Roster).filter(roster_year=settings.CURRENT_YEAR).exclude(id=roster.id)
        opposing_players = _pos_points_map([p for r in league_rosters for p in r.players.all()])
        roster_players = _pos_points_map(roster.players.all())

        results = {
            **_get_counts(opposing_players, league_rosters.count()),
            "roster": _get_counts(roster_players)
        }
        return Response(results, status=status.HTTP_200_OK)


def _pos_points_map(qs: Union[QuerySet, list]) -> dict:
    position_splits = defaultdict(list)
    for player in qs:
        position_splits[player.position].append(player.fantasy_points)

    return position_splits


def _get_counts(position_splits: dict, roster_count: int = 1) -> dict:
    totals = {"counts": {}, "points": {}}
    for pos, player_points in position_splits.items():
        pos = "RB" if pos == "FB" else pos
        totals["counts"][pos] = len(player_points) / roster_count
        totals["points"][pos] = sum(player_points) / roster_count

    return totals
