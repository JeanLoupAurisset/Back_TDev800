from django.contrib import admin
from .models import Album, Photo, MetaData

# Register your models here.

for model in [Album, Photo, MetaData]:
    admin.site.register(model)
