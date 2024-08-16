from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.api_util import BaseAPIView, string_to_list
from api.rosters.roster_serializers import RosterImportSerializer, RosterSerializer
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.player import Player
from ffl_companion.api_models.roster import Roster


class RosterView(BaseAPIView):
    model = Player

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status.HTTP_401_UNAUTHORIZED)

        roster = self.request.user.latest_roster
        if roster is None:
            return Response(f"No Rosters found for current user", status.HTTP_404_NOT_FOUND)

        serializer = RosterSerializer(roster)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status.HTTP_401_UNAUTHORIZED)

        serializer = RosterImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        player_ids = string_to_list(serializer.validated_data["player_ids"])
        players = self.get_queryset().filter(id__in=player_ids)
        if players.count() != len(player_ids):
            return Response("One or more players not found", status.HTTP_400_BAD_REQUEST)

        if roster_id := serializer.validated_data.get("roster_id"):
            roster = get_object_or_404(Roster, id=roster_id)
        else:
            roster_year = serializer.validated_data.get("roster_year")
            if not roster_year:
                return Response("Roster year required without roster id", status.HTTP_400_BAD_REQUEST)

            try:
                league = self.protected_query(LeagueSettings).get(setting_year=roster_year)
            except LeagueSettings.DoesNotExist:
                return Response("Could not find league for given year", status.HTTP_400_BAD_REQUEST)

            query_data = dict(
                roster_year=roster_year,
                league=league,
                owner=self.request.user,
            )
            try:
                roster = self.protected_query(Roster).get(**query_data)
            except Roster.DoesNotExist:
                roster = Roster.objects.create(**query_data, dataset=self.request.user.dataset)

        roster.players.set(players)
        roster.refresh_from_db()

        return Response(RosterSerializer(roster).data, status=status.HTTP_200_OK)


