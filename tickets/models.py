from django.db import models
import random
import string

class Guest(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    reservations = models.IntegerField(default=0)
    seats = models.JSONField(default=list)
    movie_id = models.IntegerField()

    @property
    def total_payment(self):
        try:
            movie = Movie.objects.get(id=self.movie_id)
            return self.reservations * movie.ticket_price
        except Movie.DoesNotExist:
            return 0

class Movie(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    hall = models.CharField(max_length=3)
    seats = models.IntegerField(default=100)
    available_seats = models.IntegerField(default=100)
    reservations = models.IntegerField(default=0, blank=True)
    photo = models.CharField(max_length=255, default="https://st2.depositphotos.com/1105977/9877/i/450/depositphotos_98775856-stock-photo-retro-film-production-accessories-still.jpg")
    ticket_price = models.DecimalField(max_digits=5, decimal_places=2)
    reservedSeats = models.JSONField(default=list, blank=True)


def generate_reservation_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(4))


class Reservation(models.Model):
    movie = models.ForeignKey('Movie', related_name='reservations_set', on_delete=models.CASCADE)
    guest = models.ForeignKey('Guest', related_name='reservations_set', on_delete=models.CASCADE)
    reservations_code = models.CharField(max_length=4, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.reservations_code:
            self.reservations_code = generate_reservation_code()
        super().save(*args, **kwargs)
