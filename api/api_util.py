from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated


def string_to_list(s: str, sep: str = ",") -> list:
    if not s:
        return []

    return [s.strip() for s in (s.strip()).split(sep)]


def get_queryset_filters(data: dict) -> dict:
    return {k: v for k, v in data.items() if v}


class BaseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    model = None

    def get_queryset(self):
        if self.model is None:
            raise AttributeError("Model must be set before calling this view")

        if hasattr(self.model, "dataset"):
            return self.model.objects.filter(dataset=self.request.user.dataset)

        return self.model.objects.all()






