from rest_framework import serializers

from ffl_companion.api_models.notification import Notification


class NotificationRequestSerializer(serializers.Serializer):
    notification_types = serializers.CharField(required=False)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = []

