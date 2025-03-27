from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

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
