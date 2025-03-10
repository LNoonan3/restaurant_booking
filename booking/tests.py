from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Table, Reservation


class BookingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.table = Table.objects.create(number=1, capacity=4, location='Window')

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Our Restaurant')

    def test_booking_options_page(self):
        response = self.client.get(reverse('booking_options'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Available Tables')

    def test_book_table(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('book_table'), {
            'table': self.table.id,
            'date': '2025-03-10',
            'time': '18:00',
            'party_size': 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('booking_confirmation'))
        self.assertEqual(Reservation.objects.count(), 1)

        # Attempt to double book the same table
        response = self.client.post(reverse('book_table'), {
            'table': self.table.id,
            'date': '2025-03-10',
            'time': '18:00',
            'party_size': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This table is already booked for the selected date and time.')
        self.assertEqual(Reservation.objects.count(), 1)

    def test_my_bookings(self):
        self.client.login(username='testuser', password='12345')
        Reservation.objects.create(table=self.table, user=self.user, date='2025-03-10', time='18:00', party_size=2)
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Bookings')

    def test_cancel_reservation(self):
        self.client.login(username='testuser', password='12345')
        reservation = Reservation.objects.create(table=self.table, user=self.user, date='2025-03-10', time='18:00', party_size=2)
        response = self.client.get(reverse('cancel_reservation', args=[reservation.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_bookings'))
        self.assertEqual(Reservation.objects.count(), 0)