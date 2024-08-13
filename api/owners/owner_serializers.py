from rest_framework import serializers

from owner.models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        exclude = []

    years_active = serializers.SerializerMethodField()

    @staticmethod
    def get_years_active(obj):
        return obj.stats.count()
