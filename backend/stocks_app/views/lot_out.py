from rest_framework import generics
from ..models import StockOutTransaction
from ..serializers import StockOutTransactionSerializer

class StockOutCreateAPIView(generics.CreateAPIView):

    queryset = StockOutTransaction.objects.all()
    serializer_class = StockOutTransactionSerializer