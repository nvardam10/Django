from rest_framework import serializers
from .models import UserDetails,MovieDetails,MovieBooking

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('__all__')

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetails
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBooking
        fields = '__all__'