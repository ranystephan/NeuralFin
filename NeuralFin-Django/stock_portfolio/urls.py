from django.urls import path
from .views import PortfolioView

urlpatterns = [
    path('portfolio', PortfolioView.as_view()),
    path('portfolio/<int:stock_id>/', PortfolioView.as_view()),
]
