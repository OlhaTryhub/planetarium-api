from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    ShowSessionViewSet,
    PlanetariumDomeViewSet,
    TicketViewSet,
    ReservationViewSet,
)

app_name = "planetarium"

router = routers.DefaultRouter()

router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("tickets", TicketViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]
