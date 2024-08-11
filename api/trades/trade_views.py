from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from ffl_companion.api_models.trades import Trade


class TradesView(BaseAPIView):
    model = Trade

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        trades = self.get_queryset()
        results = [t.get_trade_comparison() for t in trades]
        results = sorted(results, key=lambda x: x["trade_date"], reverse=True)
        return Response(results, status=status.HTTP_200_OK)
