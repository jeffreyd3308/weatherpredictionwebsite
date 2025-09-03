from rest_framework import serializers
from .models import *

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('temperature', 'pressure',  'humidity', 'dewpoint', 'wind_speed')

class CreateWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('temperature', 'pressure', 'humidity', 'dewpoint', 'wind_speed')