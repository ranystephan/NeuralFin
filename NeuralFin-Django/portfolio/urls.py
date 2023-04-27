from django.urls import path
from .views import StockListCreateView, TransactionListCreateView, StockInfoView

urlpatterns = [
    path('stocks/', StockListCreateView.as_view()),
    path('transactions/', TransactionListCreateView.as_view()),
    path('stock_info/<str:symbol>/', StockInfoView.as_view()),
]
