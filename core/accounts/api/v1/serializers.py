from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with captcha verification."""

    password1 = serializers.CharField(max_length=255, write_only=True)
    captcha = serializers.CharField(write_only=True)

    class Meta:
        """Defines model and fields used in the serializer."""
        model = User
        fields = ['email', 'password', 'password1', 'captcha']

    
    def validate(self, attrs):
        """Validates password confirmation and applies Django's password validation rules."""
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail': "passwords do not match"})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)
    
    def validate_captcha(self, value):
        """Checks if the provided captcha response is valid."""
        if not CaptchaStore.objects.filter(response=value).exists():
            raise exceptions.ValidationError("invalid captcha")
        return value
    
    def create(self, validated_data):
        """Creates a new user after removing unnecessary fields."""
        del validated_data['password1']
        del validated_data['captcha']
        return User.objects.create_user(**validated_data)
    

    def __init__(self, *args, **kwargs):
        """Initializes the serializer and generates a new captcha image."""
        super().__init__(*args, **kwargs)
        new_captcha = CaptchaStore.generate_key()
        self.fields["captcha"].help_text = f'<img src="{captcha_image_url(new_captcha)}" alt="Captcha Image"/>'
        self.captcha_key = new_captcha


 
class CustomAuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication via email and password."""
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        """Validate user credentials and return the authenticated user."""
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            # check if user is verified or not
            # if not user.is_verified:
            #     raise serializers.ValidationError(
            #         {"detail": "user is not verified"}
            #     )
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include email and user ID in JWT token response."""
    
    def validate(self, attrs):
        """Validate and add email and user ID to the token response."""
        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.pk
        return validated_data