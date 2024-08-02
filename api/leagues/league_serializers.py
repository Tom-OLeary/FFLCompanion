from rest_framework import serializers

from ffl_companion.api_models.league_settings import LeagueSettings


class LeagueSettingsRequestSerializer(serializers.Serializer):
    get_url = serializers.BooleanField(required=False)


class LeagueSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueSettings
        exclude = []
