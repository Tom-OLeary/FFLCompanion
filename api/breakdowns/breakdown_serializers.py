from rest_framework import serializers

from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class YearlyStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyTeamStats
        exclude = ["league"]

    team_owner = serializers.PrimaryKeyRelatedField(source="owner.name", read_only=True)
