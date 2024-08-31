from typing import Union

from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated


def string_to_list(s: Union[str, list], sep: str = ",") -> list:
    if isinstance(s, list):
        return s

    if not s:
        return []

    return [s.strip() for s in (s.strip()).split(sep)]


def get_queryset_filters(data: dict) -> dict:
    return {k: v for k, v in data.items() if v}


class BaseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    model = None

    AUTHENTICATION_MSG = "Not Authenticated"

    def get_queryset(self) -> QuerySet:
        if self.model is None:
            raise AttributeError("Model must be set before calling this view")

        return self.protected_query(self.model)

    def protected_query(self, model) -> QuerySet:
        """Filtered by user's allowed dataset"""

        if hasattr(model, "dataset"):
            return model.objects.filter(dataset=self.request.user.dataset)

        return model.objects.all()

    def get_object(self) -> object:
        obj = super().get_object()
        if hasattr(obj, "dataset") and obj.dataset == self.request.user.dataset:
            return obj
        else:
            raise self.model.DoesNotExist()

