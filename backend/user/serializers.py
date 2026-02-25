"""
User serializers for ADP Backend
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, InviteCode, VerificationCode, Feedback


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'phone', 'avatar', 'bio', 
                  'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_name(self, obj):
        return obj.get_full_name() or obj.email


class UserCreateSerializer(serializers.ModelSerializer):
    """User creation serializer"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'code']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        code = validated_data.pop('code', None)
        
        # If invite code is required, validate it
        if code:
            try:
                invite_code = InviteCode.objects.get(code=code)
                if invite_code.is_expired or invite_code.is_exhausted:
                    raise serializers.ValidationError("Invalid or expired invite code")
            except InviteCode.DoesNotExist:
                raise serializers.ValidationError("Invalid invite code")
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email'].split('@')[0]),
            password=validated_data['password']
        )
        
        if code:
            invite_code = InviteCode.objects.get(code=code)
            invite_code.used_count += 1
            invite_code.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data['user'] = user
        return data


class PhoneLoginSerializer(serializers.Serializer):
    """Phone login serializer"""
    
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=10)
    
    def validate(self, data):
        # Verify the code
        try:
            verification = VerificationCode.objects.filter(
                phone=data['phone'],
                code=data['code'],
                purpose='login',
                is_used=False
            ).latest('created_at')
            
            if verification.is_expired:
                raise serializers.ValidationError("Verification code expired")
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code")
        
        # Get or create user
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            raise serializers.ValidationError("User not found")
        
        data['user'] = user
        data['verification'] = verification
        return data


class RegisterSerializer(serializers.Serializer):
    """Registration serializer"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    code = serializers.CharField(max_length=10)
    username = serializers.CharField(required=False)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, data):
        # Verify the code
        try:
            verification = VerificationCode.objects.filter(
                email=data['email'],
                code=data['code'],
                purpose='register',
                is_used=False
            ).latest('created_at')
            
            if verification.is_expired:
                raise serializers.ValidationError("Verification code expired")
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code")
        
        data['verification'] = verification
        return data


class InviteCodeSerializer(serializers.ModelSerializer):
    """Invite code serializer"""
    
    created_by_email = serializers.SerializerMethodField()
    
    class Meta:
        model = InviteCode
        fields = ['id', 'code', 'description', 'max_uses', 'used_count', 
                  'expires_at', 'created_at', 'created_by_email']
        read_only_fields = ['id', 'used_count', 'created_at']
    
    def get_created_by_email(self, obj):
        return obj.created_by.email


class InviteCodeCreateSerializer(serializers.ModelSerializer):
    """Invite code creation serializer"""
    
    class Meta:
        model = InviteCode
        fields = ['code', 'description', 'max_uses', 'expires_at']


class FeedbackSerializer(serializers.ModelSerializer):
    """Feedback serializer"""
    
    class Meta:
        model = Feedback
        fields = ['id', 'content', 'contact', 'created_at']
        read_only_fields = ['id', 'created_at']


class PasswordResetSerializer(serializers.Serializer):
    """Password reset serializer"""
    
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        try:
            verification = VerificationCode.objects.filter(
                email=data['email'],
                code=data['code'],
                purpose='password_reset',
                is_used=False
            ).latest('created_at')
            
            if verification.is_expired:
                raise serializers.ValidationError("Verification code expired")
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code")
        
        data['verification'] = verification
        return data


class PasswordResetSmsSerializer(serializers.Serializer):
    """Password reset via SMS serializer"""
    
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        try:
            verification = VerificationCode.objects.filter(
                phone=data['phone'],
                code=data['code'],
                purpose='password_reset',
                is_used=False
            ).latest('created_at')
            
            if verification.is_expired:
                raise serializers.ValidationError("Verification code expired")
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code")
        
        data['verification'] = verification
        return data
