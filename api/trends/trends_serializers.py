from rest_framework import serializers

from api.breakdowns.breakdown_serializers import YearlyStatsSerializer


class TrendsSerializer(serializers.Serializer):
    team_owner = serializers.CharField()
    stats = YearlyStatsSerializer(many=True)


class TeamTrendSerializer(serializers.Serializer):
    data = TrendsSerializer(many=True)
    years = serializers.ListField(child=serializers.CharField())
