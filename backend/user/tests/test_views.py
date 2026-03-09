from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from user.models import VerificationCode, InviteCode, Feedback

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
        self.user_sync_url = reverse('user-sync')
        self.send_email_code_url = reverse('send-email-code')
        self.password_reset_url = reverse('password-reset')
        self.token_refresh_url = reverse('token-refresh')
        self.logout_url = reverse('logout')
        self.feedback_url = reverse('feedback')

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

    def test_user_sync_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'username': 'updateduser',
            'bio': 'New bio'
        }
        response = self.client.put(self.user_sync_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.bio, 'New bio')

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

    def test_send_email_code(self):
        data = {'email': 'test-code@example.com'}
        response = self.client.post(self.send_email_code_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(VerificationCode.objects.filter(email='test-code@example.com', purpose='register').exists())

    def test_password_reset_success(self):
        # 1. Create verification code
        code = '654321'
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        VerificationCode.objects.create(
            code=code,
            email=self.user.email,
            type='email',
            purpose='password_reset',
            expires_at=expires_at
        )

        # 2. Reset password
        data = {
            'email': self.user.email,
            'code': code,
            'new_password': 'new-secure-password'
        }
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. Verify password changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new-secure-password'))

    def test_refresh_token_success(self):
        # 1. Login to get refresh token
        login_data = {
            'email': 'test@example.com',
            'password': self.user_password
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['data']['refresh']

        # 2. Use refresh token
        data = {'refresh': refresh_token}
        response = self.client.post(self.token_refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feedback_submission(self):
        self.client.force_authenticate(user=self.user)
        data = {'content': 'This is test feedback'}
        response = self.client.post(self.feedback_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Feedback.objects.filter(user=self.user, content='This is test feedback').exists())

class InviteCodeTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='password123'
        )
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='password123'
        )
        self.list_url = reverse('invite-code-list')

    def test_list_invite_codes_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        InviteCode.objects.create(code='ADMIN123', created_by=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Standard DRF pagination uses 'results' directly if no envelope is added
        self.assertEqual(len(response.data['results']), 1)

    def test_list_invite_codes_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invite_code_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'code': 'NEWCODE123',
            'max_uses': 5
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # No 'data' envelope here either
        self.assertEqual(response.data['code'], 'NEWCODE123')
        self.assertEqual(InviteCode.objects.filter(code='NEWCODE123').count(), 1)
