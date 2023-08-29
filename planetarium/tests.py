from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import make_aware

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.theme = ShowTheme.objects.create(name="Space Exploration")
        self.show = AstronomyShow.objects.create(
            title="Starry Night", description="A night sky display"
        )
        self.dome = PlanetariumDome.objects.create(
            name="Dome A", rows=10, seats_in_row=12
        )
        show_time = make_aware(datetime(2023, 8, 14, 15, 30))
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=show_time
        )
        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=5,
            seat=3,
            show_session=self.session,
            reservation=self.reservation
        )

    def test_show_theme_str(self):
        self.assertEqual(str(self.theme), self.theme.name)

    def test_astronomy_show_str(self):
        self.assertEqual(str(self.show), self.show.title)

    def test_planetarium_dome_str(self):
        self.assertEqual(str(self.dome), self.dome.name)

    def test_show_session_str(self):
        expected_str = (
            f"Show: {self.show.title} - dome: {self.dome.name}, date: "
            f"{self.session.show_time.date()}"
        )
        self.assertEqual(str(self.session), expected_str)

    def test_reservation_str(self):
        expected_str = (
            f"Reservation: {self.reservation.created_at.date()}, "
            f"{self.reservation.created_at.time()}"
        )
        self.assertEqual(str(self.reservation), expected_str)

    def test_ticket_str(self):
        expected_str = (
            f"Place: (row: {self.ticket.row}, seat: {self.ticket.seat}) dome: "
            f"{self.session.planetarium_dome}"
        )
        self.assertEqual(str(self.ticket), expected_str)

    def test_ticket_validation(self):
        valid_row = 5
        valid_seat = 3
        valid_dome = self.dome
        Ticket.validate_ticket(
            valid_row, valid_seat, valid_dome, ValidationError
        )

        invalid_row = 15
        with self.assertRaises(ValidationError):
            Ticket.validate_ticket(
                invalid_row, valid_seat, valid_dome, ValidationError
            )


class ViewTestCase(APITestCase):
    def setUp(self):
        self.theme = ShowTheme.objects.create(name="Space Exploration")
        self.show = AstronomyShow.objects.create(
            title="Starry Night", description="A night sky display"
        )
        self.dome = PlanetariumDome.objects.create(
            name="Dome A", rows=10, seats_in_row=12
        )
        show_time = make_aware(datetime(2023, 8, 14, 15, 30))
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=show_time
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=5,
            seat=3,
            show_session=self.session,
            reservation=self.reservation
        )

    def test_create_reservation(self):
        url = "/api/planetarium/reservations/"
        data = {
            "user": self.user.id,
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "show_session": self.session.id
                }
            ]
        }

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_reservations(self):
        url = "/api/planetarium/reservations/"

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
