from rest_framework import serializers
from .models import User, Movie, Collection

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('uuid', 'title', 'genre')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'user', 'description')

