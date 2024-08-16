from rest_framework import serializers

from ffl_companion.api_models.roster import Roster


class RosterImportSerializer(serializers.Serializer):
    player_ids = serializers.CharField(required=True)
    roster_id = serializers.IntegerField(required=False)
    roster_year = serializers.IntegerField(required=False)


class RosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        exclude = ["dataset"]

