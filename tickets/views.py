from rest_framework import status, viewsets, filters, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializer import GuestSerializer, MovieSerializer, ReservationSerializer
from .models import Guest, Movie, Reservation

@api_view(['POST'])
def create_superuser(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_superuser(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "User created successfully",
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name']  # البحث بناءً على اسم الضيف
    authentication_classes = [TokenAuthentication]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', 'date', 'hall', 'description', 'vertical_photo',
        'sponsor_video', 'release_date', 'duration',
        'rating', 'imdb_rating', 'tags'
    ]  # البحث بناءً على جميع الحقول الهامة
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()
        return Response({"message": "Movie and related reservations deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # البحث بواسطة رمز الحجز، اسم الضيف، أو التاجات
    filter_backends = [filters.SearchFilter]
    search_fields = ['reservations_code', 'guest__full_name', 'movie__actors', 'movie__tags']

    @action(detail=False, methods=['get'], url_path='search-by-seat')
    def search_by_seat(self, request):
        seat_number = request.query_params.get('seat')
        if not seat_number:
            return Response({"detail": "Seat number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = Reservation.objects.filter(guest__seats__contains=[seat_number]).first()

            if reservation:
                response_data = {
                    "reservation_code": reservation.reservations_code,
                    "guest": {
                        "id": reservation.guest.id,
                        "full_name": reservation.guest.full_name,
                        "age": reservation.guest.age,
                        "reservations": reservation.guest.reservations,
                        "seats": reservation.guest.seats,
                        "total_payment": reservation.guest.total_payment,
                    },
                    "movie": {
                        "id": reservation.movie.id,
                        "name": reservation.movie.name,
                        "date": reservation.movie.date,
                        "time": reservation.movie.time,
                        "hall": reservation.movie.hall,
                        "seats": reservation.movie.seats,
                        "available_seats": reservation.movie.available_seats,
                        "reservations": reservation.movie.reservations,
                        "photo": reservation.movie.photo,
                        "ticket_price": reservation.movie.ticket_price,
                        "reservedSeats": reservation.movie.reservedSeats,
                        "description": reservation.movie.description,
                        "vertical_photo": reservation.movie.vertical_photo,
                        "sponsor_video": reservation.movie.sponsor_video,
                        "release_date": reservation.movie.release_date,
                        "duration": reservation.movie.duration,
                        "rating": reservation.movie.rating,
                        "imdb_rating": reservation.movie.imdb_rating,
                        "tags": reservation.movie.tags,
                        "actors": reservation.movie.actors,
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No reservation found for this seat"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        reservation_code = kwargs.get('pk')

        try:
            reservation = Reservation.objects.get(reservations_code=reservation_code)

            response_data = {
                "reservation_code": reservation.reservations_code,
                "guest": {
                    "id": reservation.guest.id,
                    "full_name": reservation.guest.full_name,
                    "age": reservation.guest.age,
                    "reservations": reservation.guest.reservations,
                    "seats": reservation.guest.seats,
                    "total_payment": reservation.guest.total_payment,
                },
                "movie": {
                    "id": reservation.movie.id,
                    "name": reservation.movie.name,
                    "date": reservation.movie.date,
                    "time": reservation.movie.time,
                    "hall": reservation.movie.hall,
                    "seats": reservation.movie.seats,
                    "available_seats": reservation.movie.available_seats,
                    "reservations": reservation.movie.reservations,
                    "photo": reservation.movie.photo,
                    "ticket_price": reservation.movie.ticket_price,
                    "reservedSeats": reservation.movie.reservedSeats,
                    "description": reservation.movie.description,
                    "vertical_photo": reservation.movie.vertical_photo,
                    "sponsor_video": reservation.movie.sponsor_video,
                    "release_date": reservation.movie.release_date,
                    "duration": reservation.movie.duration,
                    "rating": reservation.movie.rating,
                    "imdb_rating": reservation.movie.imdb_rating,
                    "tags": reservation.movie.tags,
                    "actors": reservation.movie.actors,
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return Response({"detail": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
