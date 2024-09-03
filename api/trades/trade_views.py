from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.decorators import require_token
from ffl_companion.api_models.trades import Trade


class TradesView(BaseAPIView):
    model = Trade

    @require_token
    def get(self, request):
        trades = self.get_queryset()
        results = [t.get_trade_comparison() for t in trades]
        results = sorted(results, key=lambda x: x["trade_date"], reverse=True)
        return Response(results, status=status.HTTP_200_OK)
