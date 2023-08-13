from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError


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

    def __str__(self) -> str:
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        to=AstronomyShow,
        on_delete=models.DO_NOTHING
    )
    planetarium_dome = models.ForeignKey(
        to=PlanetariumDome,
        on_delete=models.DO_NOTHING
    )
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return (f"Show: {self.astronomy_show.title} - "
                f"dome: {self.planetarium_dome.name}, "
                f"date: {self.show_time.date()}")


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return (f"Reservation: {self.created_at.date()}, "
                f"{self.created_at.time()}")

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey(
        to=ShowSession,
        on_delete=models.DO_NOTHING,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        to=Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    def __str__(self) -> str:
        return (f"Place: (row: {self.row}, seat: {self.seat}) "
                f"dome: {self.show_session.planetarium_dome}")

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for ticket_attr_value, ticket_attr_name, planetarium_dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, planetarium_dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {planetarium_dome_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        unique_together = ("show_session", "row", "seat")
        ordering = ["row", "seat"]
