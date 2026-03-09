from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from user.models import VerificationCode

User = get_user_model()

class UserViewsTest(APITestCase):
    def setUp(self):
        self.user_password = 'password123'
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password=self.user_password
        )
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.user_info_url = reverse('user-info')

    def test_login_success(self):
        data = {
            'email': 'test@example.com',
            'password': self.user_password
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_login_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_info_authenticated(self):
        # Authenticate first
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'test@example.com')

    def test_get_user_info_unauthenticated(self):
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_success(self):
        # Create a verification code first
        email = 'newuser@example.com'
        code = '123456'
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        VerificationCode.objects.create(
            code=code,
            email=email,
            type='email',
            purpose='register',
            expires_at=expires_at
        )

        data = {
            'email': email,
            'password': 'newpassword123',
            'code': code,
            'username': 'newuser'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(email=email).count(), 1)
        
        # Verify code is marked as used
        self.assertTrue(VerificationCode.objects.get(code=code, email=email).is_used)

    def test_register_invalid_code(self):
        data = {
            'email': 'newuser2@example.com',
            'password': 'newpassword123',
            'code': '999999',
            'username': 'newuser2'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
