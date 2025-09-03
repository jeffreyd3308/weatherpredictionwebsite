from django.db import models

# Create your models here.
# user = admin, password = weatherweather
class Weather(models.Model):
    temperature = models.DecimalField(default=00.00, max_digits=4, decimal_places=2) #convert all to Fahrenheit
    pressure = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    dewpoint = models.DecimalField(default=00.00, max_digits=4, decimal_places=2)
    wind_speed = models.DecimalField(default=00.00, max_digits=4, decimal_places=2)