from django.contrib.auth import get_user_model
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(
        to=ShowTheme,
        related_name="astronomy_shows"
    )


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        to=AstronomyShow,
        on_delete=models.SET_NULL
    )
    planetarium_dome = models.ForeignKey(
        to=PlanetariumDome,
        on_delete=models.SET_NULL
    )
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.DO_NOTHING)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey(
        to=ShowSession,
        on_delete=models.DO_NOTHING
    )
    reservation = models.ForeignKey(to=Reservation, on_delete=models.CASCADE)

