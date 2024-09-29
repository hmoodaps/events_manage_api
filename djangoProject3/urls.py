from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from tickets import views
from tickets.views import create_superuser

router = routers.DefaultRouter()
router.register('guests', views.GuestViewSet)
router.register('movies', views.MovieViewSet)
router.register('reservations', views.ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('viewsets/', include(router.urls)),
    path('create-superuser/', create_superuser, name='create-superuser'),
]
