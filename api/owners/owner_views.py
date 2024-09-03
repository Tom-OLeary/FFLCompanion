from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.decorators import require_token
from api.owners.owner_serializers import OwnerSerializer
from owner.models import Owner


class OwnerListView(BaseAPIView):
    model = Owner

    @require_token
    def get(self, request):
        owners = self.get_queryset()
        return Response(OwnerSerializer(owners, many=True).data, status=status.HTTP_200_OK)


class OwnerDetailView(BaseAPIView):
    queryset = Owner.objects.all()
    model = Owner
    lookup_field = "id"
    lookup_url_kwarg = "owner_id"

    @require_token
    @extend_schema(
        parameters=[OpenApiParameter(name="owner_id", location="path", type=str)],
        responses={"200": OwnerSerializer},
    )
    def get(self, request, *args, **kwargs):
        owner = self.get_object()  # TODO test config filter
        return Response(OwnerSerializer(owner).data, status=status.HTTP_200_OK)
