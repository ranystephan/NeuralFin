from django.urls import path
from . import views

urlpatterns = [
    path('stockRisk/<str:symbol>/', views.stock_risk, name='stock_risk'),
]
