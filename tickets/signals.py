from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation

@receiver(post_save, sender=Reservation)
def update_movie_reservations_on_save(sender, instance, **kwargs):
    movie = instance.movie
    movie.reservations = Reservation.objects.filter(movie=movie).count()
    movie.reservedSeats = list(set(movie.reservedSeats + instance.guest.seats))
    movie.available_seats = movie.seats - len(movie.reservedSeats)

    print(f"Reservations updated: {movie.reservations}") 
    print(f"Reserved Seats updated: {movie.reservedSeats}")
    print(f"Available Seats updated: {movie.available_seats}")

    movie.save()


@receiver(post_delete, sender=Reservation)
def update_movie_reservations_on_delete(sender, instance, **kwargs):
    movie = instance.movie
    movie.reservations = Reservation.objects.filter(movie=movie).count()
    movie.reservedSeats = [seat for seat in movie.reservedSeats if seat not in instance.guest.seats]
    movie.available_seats = movie.seats - len(movie.reservedSeats)
    movie.save()
