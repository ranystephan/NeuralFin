from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Stock
from .serializers import StockSerializer
from django.db.models import Q



class StockSearchView(generics.ListAPIView):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        queryset = Stock.objects.filter(Q(symbol__icontains=search_query) | Q(name__icontains=search_query))
        return queryset


class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    
    
class StockRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
