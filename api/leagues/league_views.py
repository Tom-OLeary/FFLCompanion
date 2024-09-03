from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.decorators import require_token
from api.leagues.league_serializers import LeagueSettingsRequestSerializer, LeagueSettingsSerializer
from ffl_companion.api_models.league_settings import LeagueSettings


class LeagueSettingsView(BaseAPIView):
    model = LeagueSettings

    @require_token
    def get(self, request):
        serializer = LeagueSettingsRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("get_url", False):
            league = self.get_queryset().order_by("-setting_year").first()
            return Response(LeagueSettingsSerializer(league).data, status=status.HTTP_200_OK)

        # TODO future update for additional filters
        return Response([], status=status.HTTP_200_OK)
