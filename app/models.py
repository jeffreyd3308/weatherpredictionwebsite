from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import time
import math
import os
import glob
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.metrics import RootMeanSquaredError
import joblib

#manually calculate dewpoint based on https://iridl.ldeo.columbia.edu/dochelp/QA/Basic/dewpoint.html simplified equation
def calculate_dew_point(temp_c, humidity_percent):
    dew_point = temp_c - ((100 - humidity_percent)/5)
    return dew_point

key = "b1aed90608b1028bb3c1cd48cd402913"
#train/test data
def fetch_weather_data(city, api_key):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    records = []

    for entry in data['list']:
        main = entry['main']
        wind = entry['wind']
        rain = entry.get('rain', {})
        dt_txt = entry['dt_txt']

        record = {
            'datetime': dt_txt,
            'temp': main['temp'],
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'wind_speed': wind['speed'],
            'dew_point': calculate_dew_point(main['temp'], main['humidity']),
            'precipitation': rain.get('3h', 0)  #millimeters over 3 hours
        }
        records.append(record)

    print(data)
    return pd.DataFrame(records)

def create_model():
    training_data = pd.read_csv('traindata/Combined.csv') #not train 80 percent variable
    x = training_data[['temp', 'pressure', 'humidity', 'dew_point', 'wind_speed']]
    y = np.log1p(training_data[['precipitation']])

    #scale to interval 0-1
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    #train80percent test20percent
    x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2)

    model = Sequential([
        Dense(64, activation='relu', input_shape=(x_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['RootMeanSquaredError'])
    model.fit(x_train, y_train, epochs=50, batch_size=16, validation_split=0.2)

    predictions = np.expm1(model.predict(x_test))
    print(predictions[:5])
    loss, rmse = model.evaluate(x_test, y_test)
    #rmse of 0.2082, interpretation-> typically our prediction of precipitation is off by about 0.2082 millimeters from our actual precipitation on average
    print(rmse)

    return model, scaler

# Create your models here.
# user = admin, password = weatherweather
class Weather(models.Model):
    temperature = models.DecimalField(default=000.00, max_digits=5, decimal_places=2)
    pressure = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    dewpoint = models.DecimalField(default=000.00, max_digits=5, decimal_places=2)
    wind_speed = models.DecimalField(default=000.00, max_digits=5, decimal_places=2)
    precipitation_prediction = models.DecimalField(default=00.000000, max_digits=8, decimal_places=6)

class Prediction(models.Model):
    prediction = models.DecimalField(default=00.000000, max_digits=8, decimal_places=6)

@receiver(post_save, sender=Weather)
def create_prediction(sender, instance, created, **kwargs):
    if created:
        print(f"signal received")
        model = load_model('MLmodels/precipitationv1.keras')
        scaler = joblib.load('MLmodels/scaler.pkl')
        input_data = np.array([[instance.temperature, instance.pressure, instance.humidity, instance.wind_speed, instance.dewpoint]])
        input_scaled = scaler.transform(input_data)
        prediction = np.expm1(model.predict(input_scaled))
        instance.precipitation_prediction = round(float(prediction[0][0]), 6)
        instance.save(update_fields=['precipitation_prediction'])
        Prediction.objects.all().delete()
        Prediction.objects.create(prediction=instance.precipitation_prediction)
        print(f"Predicted precipitation amount: {prediction[0][0]:.6f} mm {prediction[0][0]}")
