from rest_framework import serializers
from .models import People
from django.contrib.auth.models import User


class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = ('first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
