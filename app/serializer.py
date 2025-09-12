from rest_framework import serializers
from .models import *

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('temperature', 'pressure',  'humidity', 'dewpoint', 'wind_speed', 'precipitation_prediction')

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['prediction']

#testing purposes
class CreateWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('temperature', 'pressure', 'humidity', 'dewpoint', 'wind_speed', 'precipitation_prediction')