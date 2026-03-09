from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from user.models import InviteCode, VerificationCode, Feedback

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(str(user), 'test@example.com')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='password123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class InviteCodeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='creator@example.com',
            username='creator',
            password='password123'
        )

    def test_invite_code_properties(self):
        code = InviteCode.objects.create(
            code='INVITE123',
            max_uses=2,
            created_by=self.user
        )
        self.assertFalse(code.is_expired)
        self.assertFalse(code.is_exhausted)
        
        code.used_count = 2
        self.assertTrue(code.is_exhausted)

    def test_invite_code_expiration(self):
        past_time = timezone.now() - timezone.timedelta(days=1)
        code = InviteCode.objects.create(
            code='EXPIRED',
            expires_at=past_time,
            created_by=self.user
        )
        self.assertTrue(code.is_expired)

class VerificationCodeModelTest(TestCase):
    def test_verification_code_expiration(self):
        future_time = timezone.now() + timezone.timedelta(minutes=5)
        code = VerificationCode.objects.create(
            code='123456',
            email='test@example.com',
            type='email',
            purpose='register',
            expires_at=future_time
        )
        self.assertFalse(code.is_expired)
        
        past_time = timezone.now() - timezone.timedelta(minutes=5)
        expired_code = VerificationCode.objects.create(
            code='654321',
            email='test@example.com',
            type='email',
            purpose='register',
            expires_at=past_time
        )
        self.assertTrue(expired_code.is_expired)
