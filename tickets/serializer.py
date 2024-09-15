from rest_framework import serializers
from .models import Movie, Guest, Reservation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['name', 'date', 'time', 'hall', 'sets', 'available_seats', 'reservations', 'photo', 'ticket_price', 'reservedSeats']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['full_name', 'age', 'reservations', 'seats']

class ReservationSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    guest = GuestSerializer()

    class Meta:
        model = Reservation
        fields = ['movie', 'guest', 'reservations_code']
