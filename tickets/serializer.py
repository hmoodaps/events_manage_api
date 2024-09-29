from rest_framework import serializers
from .models import Movie, Guest, Reservation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'name',
            'date',
            'time',
            'hall',
            'seats',
            'available_seats',
            'reservations',
            'photo',
            'ticket_price',
            'reservedSeats',
            'description',
            'vertical_photo',
            'sponsor_video',
            'actors',
            'release_date',
            'duration',
            'rating',
            'imdb_rating',
            'tags'
        ]

class GuestSerializer(serializers.ModelSerializer):
    total_payment = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Guest
        fields = ['id', 'full_name', 'age', 'reservations', 'seats', 'total_payment']

class ReservationSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    guest = GuestSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'movie', 'guest', 'reservations_code']

    def create(self, validated_data):
        movie_data = validated_data.pop('movie')
        guest_data = validated_data.pop('guest')

        # تحقق من وجود الفيلم في قاعدة البيانات
        try:
            movie = Movie.objects.get(**movie_data)
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie": "The specified movie does not exist."})

        # تحقق من وجود الضيف في قاعدة البيانات أو قم بإنشاء ضيف جديد
        guest, created = Guest.objects.get_or_create(**guest_data)

        # إنشاء الحجز
        reservation = Reservation.objects.create(movie=movie, guest=guest, **validated_data)
        return reservation

    def update(self, instance, validated_data):
        # تحديث movie
        movie_data = validated_data.pop('movie', None)
        if movie_data:
            movie_serializer = MovieSerializer(instance.movie, data=movie_data)
            if movie_serializer.is_valid():
                movie_serializer.save()

        # تحديث guest
        guest_data = validated_data.pop('guest', None)
        if guest_data:
            guest_serializer = GuestSerializer(instance.guest, data=guest_data)
            if guest_serializer.is_valid():
                guest_serializer.save()

        # تحديث الحجز
        return super().update(instance, validated_data)
