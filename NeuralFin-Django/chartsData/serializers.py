from rest_framework import serializers
from .models import ChartData

class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartData
        fields = '__all__'