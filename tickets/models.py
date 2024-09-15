from django.db import models
import random
import string

class Movie(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    hall = models.CharField(max_length=3)
    sets = models.IntegerField(default=100)  # Number of available sets
    available_seats = models.IntegerField(default=100)  # Number of available sets
    reservations = models.IntegerField(default=0)  # Number of reservations made
    photo = models.CharField(max_length=255, default="https://st2.depositphotos.com/1105977/9877/i/450/depositphotos_98775856-stock-photo-retro-film-production-accessories-still.jpg")
    ticket_price = models.DecimalField(max_digits=5, decimal_places=2)
    reservedSeats = models.JSONField(default=list)  # List of reserved seats

class Guest(models.Model):
    objects = models.Manager()
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    reservations = models.IntegerField(default=0)  # Default value to 0
    seats = models.JSONField(default=list)  # List of seats reserved by the guest

class Reservation(models.Model):
    movie = models.ForeignKey('Movie', related_name='Reservations', on_delete=models.CASCADE)
    guest = models.ForeignKey('Guest', related_name='Reservations', on_delete=models.CASCADE)
    reservations_code = models.CharField(max_length=4, unique=True, blank=True, editable=False)
    objects = models.Manager()

    def generate_reservation_code(self):
        """Generate a random 4-character alphanumeric code."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(4))

    def save(self, *args, **kwargs):
        """Override save method to assign a unique reservation code."""
        if not self.reservations_code:
            self.reservations_code = self.generate_reservation_code()
        super().save(*args, **kwargs)
        # Update reservations count in Movie
        if self.pk:  # Ensure the reservation is already saved
            movie = self.movie
            movie.reservations = Reservation.objects.filter(movie=movie).count()  # Update reservations count correctly
            movie.save()
