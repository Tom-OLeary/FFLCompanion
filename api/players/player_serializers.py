from django.conf import settings
from rest_framework import serializers

from ffl_companion.api_models.player import NFLPlayer, Player, PlayerStatsWeekly


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
        exclude = ["nfl_teams", "common_name"]

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
        totals = obj.season_totals(year=settings.CURRENT_YEAR, fields=self._STATS_FIELDS)
        return totals or {k: 0 for k in self._STATS_FIELDS}


class PlayerStatsRequestSerializer(serializers.Serializer):
    roster_id = serializers.IntegerField(required=False)
    player_ids = serializers.CharField(required=False)
    split_type = serializers.CharField(required=False, default="total")

    def is_valid(self, *, raise_exception=False):
        if not (self.initial_data.get("roster_id") or self.initial_data.get("player_ids")):
            raise serializers.ValidationError("Request must include roster_id or player_ids")

        return super(PlayerStatsRequestSerializer, self).is_valid(raise_exception=raise_exception)


class PlayerStatsSplitsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatsWeekly
        exclude = ["game_date", "game_week", "opponent", "player"]

    player_id = serializers.SerializerMethodField()

    @staticmethod
    def get_player_id(obj):
        return obj["stats_weekly__player_id"]
