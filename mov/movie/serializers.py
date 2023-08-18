from rest_framework import serializers
from .models import User_Details,Movie_Details,Movie_Booking
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserRegisterSerializer(serializers.ModelSerializer):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User_Details
        exclude = ['date_updated','date_added']
        

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_Details
        exclude = ['date_updated','date_added']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_Booking
        exclude = ['date_updated','date_added']