
from django.urls import path
from .views import OptionsExpAPIView, OptionsChainsAPIView

urlpatterns = [
    path('exp/<str:symbol>/', OptionsExpAPIView.as_view(), name='options-exp'),
    path('chains/<str:symbol>/<str:exp_date>/', OptionsChainsAPIView.as_view(), name='options-chains'),
]
