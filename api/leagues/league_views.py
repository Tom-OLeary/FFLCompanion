from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.leagues.league_serializers import LeagueSettingsRequestSerializer, LeagueSettingsSerializer
from ffl_companion.api_models.league_settings import LeagueSettings


class LeagueSettingsView(GenericAPIView):
    queryset = LeagueSettings.objects.all()

    def get_queryset(self):
        return LeagueSettings.objects.all()

    def get(self, request):
        serializer = LeagueSettingsRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("get_url", False):
            league = self.get_queryset().order_by("-setting_year").first()
            return Response(LeagueSettingsSerializer(league).data, status=status.HTTP_200_OK)

        # TODO future update for additional filters
        return Response([], status=status.HTTP_200_OK)
