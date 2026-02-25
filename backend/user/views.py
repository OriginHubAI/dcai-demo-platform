"""
User views for ADP Backend
"""
import random
import string
import secrets
from django.utils import timezone
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import User, InviteCode, VerificationCode, Feedback
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    PhoneLoginSerializer, RegisterSerializer, InviteCodeSerializer,
    InviteCodeCreateSerializer, FeedbackSerializer,
    PasswordResetSerializer, PasswordResetSmsSerializer
)


def generate_verification_code(length=6):
    """Generate random verification code"""
    return ''.join(random.choices(string.digits, k=length))


def send_email_code(email, code):
    """Send email verification code (placeholder)"""
    # TODO: Implement email sending
    print(f"Sending email verification code {code} to {email}")
    return True


def send_sms_code(phone, code):
    """Send SMS verification code (placeholder)"""
    # TODO: Implement SMS sending
    print(f"Sending SMS verification code {code} to {phone}")
    return True


class UserInfoView(APIView):
    """Get current user info"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'code': 0,
            'msg': 'success',
            'data': serializer.data
        })


class UserSyncView(APIView):
    """Sync/update user info"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 0,
                'msg': 'success',
                'data': serializer.data
            })
        return Response({
            'code': 100001,
            'msg': 'Validation error',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Email/password login"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }
            })
        return Response({
            'code': 100001,
            'msg': 'Invalid credentials',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PhoneLoginView(APIView):
    """Phone/SMS login"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PhoneLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            verification = serializer.validated_data['verification']
            verification.is_used = True
            verification.save()
            
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }
            })
        return Response({
            'code': 100001,
            'msg': 'Invalid verification code',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SendSmsCodeView(APIView):
    """Send login SMS verification code"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({
                'code': 100001,
                'msg': 'Phone number required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        code = generate_verification_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        VerificationCode.objects.create(
            code=code,
            phone=phone,
            type='phone',
            purpose='login',
            expires_at=expires_at
        )
        
        send_sms_code(phone, code)
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class RegisterView(APIView):
    """User registration"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Create user
            user_data = serializer.validated_data
            user = User.objects.create_user(
                email=user_data['email'],
                username=user_data.get('username', user_data['email'].split('@')[0]),
                password=user_data['password']
            )
            
            # Mark verification code as used
            verification = serializer.validated_data['verification']
            verification.is_used = True
            verification.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }
            })
        return Response({
            'code': 100001,
            'msg': 'Registration failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SendEmailCodeView(APIView):
    """Send email verification code"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                'code': 100001,
                'msg': 'Email required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        code = generate_verification_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        VerificationCode.objects.create(
            code=code,
            email=email,
            type='email',
            purpose='register',
            expires_at=expires_at
        )
        
        send_email_code(email, code)
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class SendSmsCodeRegisterView(APIView):
    """Send SMS verification code for registration"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({
                'code': 100001,
                'msg': 'Phone number required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        code = generate_verification_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        VerificationCode.objects.create(
            code=code,
            phone=phone,
            type='phone',
            purpose='register',
            expires_at=expires_at
        )
        
        send_sms_code(phone, code)
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class SendPasswordResetCodeView(APIView):
    """Send password reset email code"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                'code': 100001,
                'msg': 'Email required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(email=email).exists():
            return Response({
                'code': 100002,
                'msg': 'User not found',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)
        
        code = generate_verification_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        VerificationCode.objects.create(
            code=code,
            email=email,
            type='email',
            purpose='password_reset',
            expires_at=expires_at
        )
        
        send_email_code(email, code)
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class SendPasswordResetSmsCodeView(APIView):
    """Send password reset SMS code"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({
                'code': 100001,
                'msg': 'Phone number required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(phone=phone).exists():
            return Response({
                'code': 100002,
                'msg': 'User not found',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)
        
        code = generate_verification_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
        VerificationCode.objects.create(
            code=code,
            phone=phone,
            type='phone',
            purpose='password_reset',
            expires_at=expires_at
        )
        
        send_sms_code(phone, code)
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class PasswordResetView(APIView):
    """Reset password via email"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            verification = serializer.validated_data['verification']
            verification.is_used = True
            verification.save()
            
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {}
            })
        return Response({
            'code': 100001,
            'msg': 'Password reset failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetSmsView(APIView):
    """Reset password via SMS"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSmsSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(phone=serializer.validated_data['phone'])
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            verification = serializer.validated_data['verification']
            verification.is_used = True
            verification.save()
            
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {}
            })
        return Response({
            'code': 100001,
            'msg': 'Password reset failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """Refresh access token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'code': 100001,
                'msg': 'Refresh token required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        except Exception as e:
            return Response({
                'code': 100001,
                'msg': 'Invalid refresh token',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # In a more complete implementation, we would blacklist the token
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class InviteCodeViewSet(viewsets.ModelViewSet):
    """Invite code CRUD"""
    serializer_class = InviteCodeSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return InviteCode.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InviteCodeCreateSerializer
        return InviteCodeSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeedbackView(APIView):
    """Submit user feedback"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'code': 0,
                'msg': 'success',
                'data': serializer.data
            })
        return Response({
            'code': 100001,
            'msg': 'Feedback submission failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Placeholder views for OAuth - will be implemented later
class WechatQRGenerateView(APIView):
    """Generate WeChat QR code"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # TODO: Implement WeChat OAuth
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {'qr_url': 'https://example.com/wechat/qr'}
        })


class WechatQRStatusView(APIView):
    """Check WeChat QR status"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # TODO: Implement WeChat OAuth
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {'status': 'waiting'}
        })


class WechatCallbackView(APIView):
    """WeChat OAuth callback"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # TODO: Implement WeChat OAuth callback
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })


class GithubAuthGenerateView(APIView):
    """Generate GitHub auth URL"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # TODO: Implement GitHub OAuth
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {'auth_url': 'https://github.com/login/oauth/authorize'}
        })


class GithubAuthStatusView(APIView):
    """Check GitHub auth status"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # TODO: Implement GitHub OAuth
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {'status': 'waiting'}
        })


class GithubCallbackView(APIView):
    """GitHub OAuth callback"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # TODO: Implement GitHub OAuth callback
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {}
        })
