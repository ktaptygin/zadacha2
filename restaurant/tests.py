from django.test import TestCase, override_settings
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils import timezone
from .models import Booking, Contact, UserProfile
# Create your tests here.

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='test@example.com',
    RESTAURANT_EMAIL='restaurant@example.com',
)
class RestaurantViewsTests(TestCase):
    def test_index_opens(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_valid_booking_is_saved_and_email_is_sent(self):
        booking_date = timezone.localdate() + timedelta(days=1)
        response = self.client.post(reverse('create_booking'), {
            'name': 'Test Guest',
            'email': 'guest@example.com',
            'phone': '+123456789',
            'people': '2',
            'date': booking_date.isoformat(),
            'time': '20:00',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['email_sent'])
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['restaurant@example.com'])

    def test_invalid_booking_date_returns_400(self):
        response = self.client.post(reverse('create_booking'), {
            'name': 'Test Guest',
            'email': 'guest@example.com',
            'phone': '+123456789',
            'people': '2',
            'date': 'not-a-date',
            'time': '20:00',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Booking.objects.count(), 0)

    def test_contact_message_is_saved(self):
        response = self.client.post(reverse('create_contact'), {
            'name': 'Test Guest',
            'email': 'guest@example.com',
            'phone': '+123456789',
            'message': 'Hello',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)

    def test_registration_saves_phone_in_profile(self):
        response = self.client.post(reverse('register_user'), {
            'full_name': 'Test User',
            'email': 'user@example.com',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!',
            'phone': '+123456789',
        })
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(username='user@example.com')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.phone, '+123456789')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)