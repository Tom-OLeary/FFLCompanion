from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.owners.owner_serializers import TeamOwnerSerializer
from ffl_companion.api_models.owner import TeamOwner


class TeamOwnerListView(GenericAPIView):
    queryset = TeamOwner.objects.all()

    def get(self, request):
        owners = self.get_queryset()  # TODO test config filter
        return Response(TeamOwnerSerializer(owners, many=True).data, status=status.HTTP_200_OK)


class TeamOwnerDetailView(GenericAPIView):
    queryset = TeamOwner.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "owner_id"

    @extend_schema(
        parameters=[OpenApiParameter(name="owner_id", location="path", type=str)],
        responses={"200": TeamOwnerSerializer},
    )
    def get(self, request, *args, **kwargs):
        owner = self.get_object()  # TODO test config filter
        return Response(TeamOwnerSerializer(owner).data, status=status.HTTP_200_OK)
