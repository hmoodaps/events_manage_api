from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation

@receiver(post_save, sender=Reservation)
def update_movie_reservations(sender, instance, **kwargs):
    # الحصول على الفيلم المرتبط بالحجز
    movie = instance.movie
    # حساب عدد الحجوزات المرتبطة بالفيلم
    movie.reservations = Reservation.objects.filter(movie=movie).count()
    # حفظ الفيلم مع العدد المحدث للحجوزات
    movie.save()

@receiver(post_delete, sender=Reservation)
def update_movie_reservations_on_delete(sender, instance, **kwargs):
    movie = instance.movie
    # حساب عدد الحجوزات الحالية للفيلم بعد الحذف
    movie.reservations = Reservation.objects.filter(movie=movie).count()
    # حفظ الفيلم مع العدد المحدث للحجوزات
    movie.save()
