from django.contrib import admin
from django.apps import apps
from .models import *

# Register your models here.
for model in apps.get_app_config('app').get_models():
    admin.site.register(model)