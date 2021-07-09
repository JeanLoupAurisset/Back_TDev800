from rest_framework import serializers
from .models import Album, Photo, MetaData
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .configfile import limit_payment_trial, limit_amount
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','password', 'first_name', 'email', 'date_joined')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user

class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class MetaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaData
        fields = ('id', 'type', 'valeur', 'mode_acquisition', 'date_ajout', 'photo_id')
    
    def create(self, validated_data):
        validated_data['photo_id'] = self.context['request'].GET['photo_id']
        obj = MetaData.objects.create(**validated_data)
        obj.save()
        return obj

class PhotoSerializer(serializers.ModelSerializer):
    metadatas = MetaDataSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'images', 'name', 'metadatas', 'album_id')

    def create(self, validated_data):
        validated_data['album_id'] = self.context['request'].GET['album_id']
        obj = Photo.objects.create(**validated_data)
        obj.save()
        return obj

class AlbumSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'Access_public', 'user_id', 'photos',)

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        obj = Album.objects.create(**validated_data)
        obj.save()
        return obj


        
