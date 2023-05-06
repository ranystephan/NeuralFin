from django.urls import path
from .views import (PortfolioListCreateView, PortfolioRetrieveUpdateDestroyView,
                    PortfolioItemListCreateView, PortfolioItemRetrieveUpdateDestroyView, PortfolioMetricsView)

urlpatterns = [
    path('portfolios/', PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolios/<int:pk>/', PortfolioRetrieveUpdateDestroyView.as_view(), name='portfolio-retrieve-update-destroy'),
    path('portfolio-items/', PortfolioItemListCreateView.as_view(), name='portfolio-item-list-create'),
    path('portfolio-items/<int:pk>/', PortfolioItemRetrieveUpdateDestroyView.as_view(), name='portfolio-item-retrieve-update-destroy'),
    path('portfolio-metrics/', PortfolioMetricsView.as_view(), name='portfolio-metrics'),
]
