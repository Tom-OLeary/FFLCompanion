from django.conf import settings
from rest_framework import serializers

from ffl_companion.api_models.player import NFLPlayer, Player


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
        exclude = ["owner"]


class PlayerSearchSerializer(serializers.Serializer):
    QB = serializers.ListSerializer(child=serializers.CharField())
    RB = serializers.ListSerializer(child=serializers.CharField())
    WR = serializers.ListSerializer(child=serializers.CharField())
    TE = serializers.ListSerializer(child=serializers.CharField())
    DEF = serializers.ListSerializer(child=serializers.CharField())
    players = serializers.ListSerializer(child=serializers.CharField(), required=False)


class PlayerSearchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ["nfl_teams"]

    team = serializers.CharField(source="current_team.abbreviation", default=None, read_only=True)


class PlayerTotalsResponseSerializer(serializers.ModelSerializer):
    _STATS_FIELDS = [
        "pass_attempts",
        "pass_completions",
        "pass_yds",
        "pass_td",
        "interceptions",
        "rush_attempts",
        "rush_yds",
        "rush_td",
        "targets",
        "receptions",
        "receiving_yards",
        "receiving_td",
    ]

    class Meta:
        model = Player
        exclude = ["nfl_teams"]

    team = serializers.CharField(source="current_team.abbreviation", default=None, read_only=True)
    stats = serializers.SerializerMethodField()

    def get_stats(self, obj):
        return obj.season_totals(year=settings.CURRENT_YEAR, fields=self._STATS_FIELDS)
