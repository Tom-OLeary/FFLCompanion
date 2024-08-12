from rest_framework import serializers

from api.breakdowns.breakdown_serializers import YearlyStatsSerializer


class StatsSerializer(YearlyStatsSerializer):
    class Meta(YearlyStatsSerializer.Meta):
        exclude = ["id", "dataset", "league", "league_name"]


class TrendsSerializer(serializers.Serializer):
    team_owner = serializers.CharField()
    stats = StatsSerializer(many=True)


class TeamTrendSerializer(serializers.Serializer):
    data = TrendsSerializer(many=True)
    years = serializers.ListField(child=serializers.CharField())
    columns = serializers.ListField(child=serializers.CharField())
