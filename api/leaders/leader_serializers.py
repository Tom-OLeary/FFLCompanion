from rest_framework import serializers

from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


class ReigningChampsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyTeamStats
        fields = ["team_name", "season_start_year", "owner_name"]

    owner_name = serializers.PrimaryKeyRelatedField(source="team_owner.name", required=False, default=None, read_only=True)
