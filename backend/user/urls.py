"""
User URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'invite-codes', views.InviteCodeViewSet, basename='invite-code')

urlpatterns = [
    # User info
    path('users/info', views.UserInfoView.as_view(), name='user-info'),
    path('users/sync', views.UserSyncView.as_view(), name='user-sync'),
    
    # Authentication
    path('login', views.LoginView.as_view(), name='login'),
    path('login/phone', views.PhoneLoginView.as_view(), name='phone-login'),
    path('login/sms/code', views.SendSmsCodeView.as_view(), name='send-login-sms'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('register/sms', views.RegisterView.as_view(), name='register-sms'),
    path('email/code', views.SendEmailCodeView.as_view(), name='send-email-code'),
    path('sms/code', views.SendSmsCodeRegisterView.as_view(), name='send-sms-code'),
    path('password/reset/code', views.SendPasswordResetCodeView.as_view(), name='send-password-reset-code'),
    path('password/reset/code/sms', views.SendPasswordResetSmsCodeView.as_view(), name='send-password-reset-sms'),
    path('password/reset', views.PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/sms', views.PasswordResetSmsView.as_view(), name='password-reset-sms'),
    path('refresh', views.RefreshTokenView.as_view(), name='token-refresh'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    
    # Feedback
    path('feedback', views.FeedbackView.as_view(), name='feedback'),
    
    # WeChat OAuth
    path('wechat/qr/generate', views.WechatQRGenerateView.as_view(), name='wechat-qr-generate'),
    path('wechat/qr/status', views.WechatQRStatusView.as_view(), name='wechat-qr-status'),
    path('wechat/callback', views.WechatCallbackView.as_view(), name='wechat-callback'),
    
    # GitHub OAuth
    path('github/auth/generate', views.GithubAuthGenerateView.as_view(), name='github-auth-generate'),
    path('github/auth/status', views.GithubAuthStatusView.as_view(), name='github-auth-status'),
    path('github/callback', views.GithubCallbackView.as_view(), name='github-callback'),
    
    # Router URLs
    path('', include(router.urls)),
]
