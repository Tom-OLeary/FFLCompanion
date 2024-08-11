from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.owners.owner_serializers import TeamOwnerSerializer
from ffl_companion.api_models.owner import TeamOwner


class TeamOwnerListView(BaseAPIView):
    model = TeamOwner

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        owners = self.get_queryset()
        return Response(TeamOwnerSerializer(owners, many=True).data, status=status.HTTP_200_OK)


class TeamOwnerDetailView(BaseAPIView):
    queryset = TeamOwner.objects.all()
    model = TeamOwner
    lookup_field = "id"
    lookup_url_kwarg = "owner_id"

    @extend_schema(
        parameters=[OpenApiParameter(name="owner_id", location="path", type=str)],
        responses={"200": TeamOwnerSerializer},
    )
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        owner = self.get_object()  # TODO test config filter
        return Response(TeamOwnerSerializer(owner).data, status=status.HTTP_200_OK)
