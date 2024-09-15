from rest_framework import status, viewsets, filters, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *  # تأكد من أن الاستيراد هنا صحيح

@api_view(['POST'])
def create_superuser(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_superuser(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "User created successfully",
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['__all__']
    authentication_classes = [TokenAuthentication]

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'date', 'hall']  # حدد الحقول التي تريد البحث فيها
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        movie_data = request.data.get('movie')
        guest_data = request.data.get('guest')
        seats = request.data.get('seats', [])  # List of seats

        movie_qs = Movie.objects.filter(
            name=movie_data.get('name'),
            hall=movie_data.get('hall'),
            date=movie_data.get('date'),
            time=movie_data.get('time'),
            ticket_price=movie_data.get('ticket_price')
        )

        if movie_qs.exists():
            movie = movie_qs.first()  # Use existing movie
        else:
            movie = Movie.objects.create(**movie_data)  # Create new movie

        guest_qs = Guest.objects.filter(
            full_name=guest_data.get('full_name'),
            age=guest_data.get('age')
        )

        if guest_qs.exists():
            guest = guest_qs.first()  # Use existing guest
        else:
            guest = Guest.objects.create(**guest_data, seats=seats)  # Create new guest with seats

        # Check for seat availability
        reserved_seats = set(guest.seats)
        if reserved_seats & set(seats):
            return Response({"detail": "Some of the requested seats are already reserved"}, status=status.HTTP_400_BAD_REQUEST)

        reservation_qs = Reservation.objects.filter(movie=movie, guest=guest)
        if reservation_qs.exists():
            return Response({"detail": "Reservation already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Reservation instance
        reservation = Reservation.objects.create(movie=movie, guest=guest)

        # Update reservations count in Movie
        movie.reservations = Reservation.objects.filter(movie=movie).count()  # Update reservations count correctly
        movie.save()

        # Prepare response data including movie and guest info
        response_data = {
            "reservation_code": reservation.reservations_code,
            "movie": {
                "name": movie.name,
                "date": movie.date,
                "time": movie.time,
                "hall": movie.hall,
                "sets": movie.sets,
                "available_seats": movie.available_seats,
                "reservations": movie.reservations,
                "photo": movie.photo,
                "ticket_price": movie.ticket_price
            },
            "guest": {
                "full_name": guest.full_name,
                "age": guest.age,
                "reservations": guest.reservations,
                "seats": guest.seats
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
