"""NeuralFin_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from chartsData.views import ChartAPIView


router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('summarized-news/', include('summarized_news.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('', include(router.urls)),
    
    
    path('api/stock/', include('stocks.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/charts/<str:symbol>/', ChartAPIView.as_view()),

    path('api/options/', include('options.urls')),
    
    path('api/risk/', include('stockRisk.urls')),



]
