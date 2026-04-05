from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import Profile


class RegisterViewTests(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_successful_registration_creates_user_and_profile(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        self.client.post(reverse('register'), data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(username='existing', email='dupe@example.com', password='pass123')
        data = {
            'username': 'newuser',
            'email': 'dupe@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(reverse('register'), data)
        # Form should re-render with errors, not redirect
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())


class LoginViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser',
            password='TestPass123!',
        )

    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'TestPass123!',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_with_wrong_password_shows_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='profileuser',
            password='TestPass123!',
        )

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/users/login/?next=/users/profile/')

    def test_profile_update_saves_name(self):
        self.client.login(username='profileuser', password='TestPass123!')
        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Test',
            'last_name': 'User',
            'currency': 'EUR',
            'email_notifications': True,
        })
        # Should redirect after successful save
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
