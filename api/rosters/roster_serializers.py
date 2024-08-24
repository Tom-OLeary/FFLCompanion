from rest_framework import serializers

from api.players.player_serializers import PlayerTotalsResponseSerializer
from ffl_companion.api_models.roster import Roster


class RosterImportSerializer(serializers.Serializer):
    player_ids = serializers.ListSerializer(child=serializers.CharField(), required=True)


class RosterDetailRequestSerializer(serializers.Serializer):
    latest = serializers.BooleanField(required=False)
    roster_id = serializers.IntegerField(required=False)


class RosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        exclude = ["dataset"]

    player_limit = serializers.IntegerField(default=0, read_only=True)
    players = PlayerTotalsResponseSerializer(many=True, read_only=True)
