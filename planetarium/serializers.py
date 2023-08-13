from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    Ticket,
    Reservation
)


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["show_session"].planetarium_dome,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = "__all__"


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = "__all__"


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = "__all__"


class ShowThemesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("name",)


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = "__all__"


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class ShowSessionListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        source="astronomy_show.title",
        read_only=True
    )
    description = serializers.CharField(
        source="astronomy_show.description",
        read_only=True
    )
    show_themes = serializers.StringRelatedField(
        source="astronomy_show.show_theme", many=True, read_only=True
    )
    dome_name = serializers.CharField(
        source="planetarium_dome.name",
        read_only=True
    )
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = ShowSession
        fields = (
            "title",
            "show_themes",
            "show_time",
            "description",
            "dome_name",
            "taken_places",
        )
