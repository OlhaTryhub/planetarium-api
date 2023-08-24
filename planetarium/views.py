from django.db.models import F, Count
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils import timezone

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    Reservation, Ticket
)
from planetarium.permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    IsAdminOrIfAuthenticatedReadCreateDeleteOnly
)
from planetarium.serializers import (
    ReservationSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    AstronomyShowSerializer,
    ShowThemeSerializer, ShowSessionListSerializer, ReservationListSerializer
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
        "astronomy_show", "planetarium_dome"
    ).annotate(
        tickets_available=(
            F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
            - Count("tickets")
        )
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


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_session__astronomy_show",
        "tickets__show_session__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadCreateDeleteOnly,)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Reservation.objects.filter(user=self.request.user)
        return Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        tickets = Ticket.objects.prefetch_related(
            "show_session", "reservation"
        ).filter(reservation=instance)
        current_datetime = timezone.now()

        if not self.request.user.is_staff:
            for ticket in tickets:
                if ticket.show_session.show_time < current_datetime:
                    return Response(
                        {"error": "Cannot delete reservation for past shows."},
                        status=status.HTTP_403_FORBIDDEN
                    )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer
