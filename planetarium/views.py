from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    Ticket,
    Reservation
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import (
    ReservationSerializer,
    TicketSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    AstronomyShowSerializer,
    ShowThemeSerializer, ShowSessionListSerializer
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminUser,)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminUser,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.prefetch_related(
        "astronomy_show",
        "planetarium_dome"
    )
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        return ShowSessionSerializer



class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminUser,)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Reservation.objects.filter(user=self.request.user)
        return Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)