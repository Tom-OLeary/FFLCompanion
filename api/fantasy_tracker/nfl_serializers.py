from rest_framework import serializers

from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.api_models.player import NFLPlayer
from ffl_companion.api_models.trades import Trade


class PlayerRequestSerializer(serializers.Serializer):
    stat_type = serializers.ChoiceField(required=False, choices=NFLPlayer.StatTypeChoices.choices)
    positions = serializers.CharField(required=False)
    teams = serializers.CharField(required=False)
    min_pass_yards = serializers.IntegerField(required=False)
    min_rush_yards = serializers.IntegerField(required=False)
    min_pass_attempts = serializers.IntegerField(required=False)
    min_rush_attempts = serializers.IntegerField(required=False)
    min_targets = serializers.IntegerField(required=False)
    min_receptions = serializers.IntegerField(required=False)
    min_receiving_yards = serializers.IntegerField(required=False)
    season_start_year = serializers.IntegerField(required=False)
    is_available = serializers.BooleanField(required=False)
    fantasy_team_ids = serializers.CharField(required=False)
    fantasy_team_names = serializers.CharField(required=False)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLPlayer
        exclude = []

    fantasy_team_name = serializers.PrimaryKeyRelatedField(source="fantasy_team.team_name", required=False, default=None, read_only=True)


class TeamOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamOwner
        exclude = []

    years_active = serializers.SerializerMethodField()

    @staticmethod
    def get_years_active(obj):
        return obj.team_stats.count()


class ReigningChampsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyTeamStats
        fields = ["team_name", "season_start_year", "owner_name"]

    owner_name = serializers.PrimaryKeyRelatedField(source="team_owner.name", required=False, default=None, read_only=True)


class LeagueSettingsRequestSerializer(serializers.Serializer):
    get_url = serializers.BooleanField(required=False)


class LeagueSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueSettings
        exclude = []


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = []
