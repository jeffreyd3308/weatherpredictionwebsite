from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializer import *
from django.shortcuts import redirect

# Create your views here.

def redirect_to_frontend(request):
    return redirect('https://jeffreyd3308.github.io')



class WeatherView(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

class PredictionView(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

#for testing purposes
class CreateWeatherView(APIView):
    serializer_class = CreateWeatherSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            temperature = serializer.data.get('temperature')
            pressure = serializer.data.get('pressure')
            humidity = serializer.data.get('humidity')
            dewpoint = serializer.data.get('dewpoint')
            wind_speed = serializer.data.get('wind_speed')
            precipitation_prediction = serializer.data.get('precipitation_prediction')
            weather = Weather(temperature=temperature, pressure=pressure, humidity=humidity, dewpoint=dewpoint, wind_speed=wind_speed, precipitation_prediction=precipitation_prediction)
            weather.save()
            return Response(WeatherSerializer(weather).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
