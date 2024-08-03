from rest_framework import serializers

from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class ReigningChampsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyTeamStats
        fields = ["team_name", "season_start_year", "owner_name"]

    owner_name = serializers.PrimaryKeyRelatedField(source="team_owner.name", required=False, default=None, read_only=True)


class LeaderPayloadSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    team_name = serializers.CharField(required=True)
    total = serializers.FloatField(required=True)
    is_active = serializers.BooleanField(required=True)
    category_type = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    image = serializers.CharField(required=True)
    years_count = serializers.IntegerField(required=True)


class LeagueLeadersSerializer(serializers.Serializer):
    titles = LeaderPayloadSerializer(many=True)
    points = LeaderPayloadSerializer(many=True)
    wins = LeaderPayloadSerializer(many=True)