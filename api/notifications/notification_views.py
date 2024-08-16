from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView, string_to_list
from api.notifications.notification_serializers import NotificationSerializer, NotificationRequestSerializer
from ffl_companion.api_models.notification import Notification
from owner.models import Owner


class NotificationAlertsView(BaseAPIView):
    model = Notification

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        serializer = NotificationRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        query_params = {"notification_type__in": [Notification.NotificationType.ALERT]}
        notification_types = string_to_list(serializer.validated_data.get("notification_types"))
        if notification_types:
            query_params["notification_type__in"] = notification_types

        notifications = self.get_queryset().filter(**query_params, expires_at__gte=timezone.now)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationUserView(BaseAPIView):
    model = Owner
    lookup_field = "id"
    lookup_url_kwarg = "owner_id"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        owner = self.get_object()
        notifications = owner.notifications.filter(expires_at__gte=timezone.now())
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
