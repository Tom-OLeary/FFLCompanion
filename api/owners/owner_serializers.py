from rest_framework import serializers

from ffl_companion.api_models.owner import TeamOwner


class TeamOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamOwner
        exclude = []

    years_active = serializers.SerializerMethodField()

    @staticmethod
    def get_years_active(obj):
        return obj.team_stats.count()
