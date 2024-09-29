from django.db import models
import random
import string

class Guest(models.Model):
    full_name = models.CharField(max_length=100)  # نص
    age = models.IntegerField()  # عدد صحيح
    seats = models.JSONField(default=list)  # مصفوفة
    reservations = models.IntegerField(default=0)

    @property
    def total_payment(self):
        try:
            movie = Movie.objects.get(id=self.movie_id)
            return self.reservations * movie.ticket_price
        except Movie.DoesNotExist:
            return 0

class Movie(models.Model):
    name = models.CharField(max_length=100)  # نص
    date = models.DateField()  # نص
    time = models.TimeField()  # نص
    hall = models.CharField(max_length=3)  # نص
    seats = models.IntegerField(default=100)  # عدد صحيح
    available_seats = models.JSONField(default=list)  # مصفوفة
    reservations = models.IntegerField(default=0, blank=True)  # عدد صحيح
    photo = models.CharField(max_length=255, default="https://st2.depositphotos.com/1105977/9877/i/450/depositphotos_98775856-stock-photo-retro-film-production-accessories-still.jpg")  # نص
    ticket_price = models.DecimalField(max_digits=5, decimal_places=2)  # عدد عشري
    reservedSeats = models.JSONField(default=list, blank=True)  # مصفوفة
    description = models.TextField(blank=True)  # نص
    vertical_photo = models.CharField(max_length=255, blank=True)  # نص
    sponsor_video = models.URLField(blank=True)  # نص
    actors = models.JSONField(default=list, blank=True)  # مصفوفة
    release_date = models.DateField(blank=True, null=True)  # نص
    duration = models.CharField(max_length=50, blank=True)  # نص
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # عدد عشري
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # عدد عشري
    tags = models.JSONField(default=list, blank=True)  # مصفوفة

    def __str__(self):
        return self.name

class Reservation(models.Model):
    movie = models.ForeignKey('Movie', related_name='reservations_set', on_delete=models.CASCADE)
    guest = models.ForeignKey('Guest', related_name='reservations_set', on_delete=models.CASCADE)
    reservations_code = models.CharField(max_length=4, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.reservations_code:
            self.reservations_code = generate_reservation_code()
        super().save(*args, **kwargs)

def generate_reservation_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(4))
