from rest_framework import serializers

from ffl_companion.api_models.trades import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = []
