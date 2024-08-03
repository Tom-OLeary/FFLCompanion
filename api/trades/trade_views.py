from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ffl_companion.api_models.trades import Trade


class TradesView(GenericAPIView):
    queryset = Trade.objects.all()

    def get(self, request):
        # TODO test config filter
        trades = Trade.objects.all()
        results = []
        for t in trades:
            results.append(t.get_trade_comparison())
        # serializer = TradeSerializer(trades, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        results = sorted(results, key=lambda x: x["trade_date"], reverse=True)
        return Response(results, status=status.HTTP_200_OK)
