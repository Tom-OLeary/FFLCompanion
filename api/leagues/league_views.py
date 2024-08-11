from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.leagues.league_serializers import LeagueSettingsRequestSerializer, LeagueSettingsSerializer
from ffl_companion.api_models.league_settings import LeagueSettings


class LeagueSettingsView(BaseAPIView):
    model = LeagueSettings

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        serializer = LeagueSettingsRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("get_url", False):
            league = self.get_queryset().order_by("-setting_year").first()
            return Response(LeagueSettingsSerializer(league).data, status=status.HTTP_200_OK)

        # TODO future update for additional filters
        return Response([], status=status.HTTP_200_OK)
