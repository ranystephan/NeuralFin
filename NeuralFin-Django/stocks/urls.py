from django.urls import path
from .views import StockListCreateView, StockRetrieveDestroyView, StockSearchView


urlpatterns = [
    path('stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('stocks/<int:pk>/', StockRetrieveDestroyView.as_view(), name='stock-retrieve-destroy'),
    path('stocks/search/', StockSearchView.as_view(), name='stock-search'),
]