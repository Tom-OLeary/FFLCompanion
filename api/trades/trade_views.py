from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ffl_companion.api_models.trades import Trade


class TradesView(GenericAPIView):
    def get_queryset(self):
        return Trade.objects.all()

    def get(self, request):
        trades = self.get_queryset()
        results = [t.get_trade_comparison() for t in trades]
        results = sorted(results, key=lambda x: x["trade_date"], reverse=True)
        return Response(results, status=status.HTTP_200_OK)
