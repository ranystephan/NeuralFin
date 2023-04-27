from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')

urlpatterns = [
    path('', include(router.urls)),
    path('add_stock/<int:pk>/', PortfolioViewSet.as_view({'post': 'add_stock'}), name='portfolio-add-stock'),
    path('remove_stock/<int:pk>/', PortfolioViewSet.as_view({'post': 'remove_stock'}), name='portfolio-remove-stock'),
]
