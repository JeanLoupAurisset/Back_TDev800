from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Album(models.Model):
    """Album model linked to user model"""
    name = models.CharField(default='Card', max_length=100, unique=True)
    Access_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)

class Photo(models.Model):
    """Photo model linked to album model"""
    images = models.ImageField()
    name = models.CharField(default='Card', max_length=100, unique=True)
    album = models.ForeignKey(Album,  related_name='photos', on_delete=models.CASCADE)

class MetaData(models.Model):
    """Metadata model linked to photo model"""
    type = models.CharField(default='Card', max_length=100, unique=True)
    valeur = models.CharField(default='Card', max_length=100, unique=True)
    mode_acquisition = models.CharField(default='Card', max_length=100, unique=False)
    date_ajout = models.DateField(auto_now=True)
    photo = models.ForeignKey(Photo, related_name='metadatas', on_delete=models.CASCADE)
