from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core import exceptions
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


from ....models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    email = serializers.CharField(source="user.email", read_only=True)
    captcha = serializers.CharField(write_only=True)

    class Meta:
        """Meta class defining model and fields to be serialized."""

        model = Profile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "description",
            "captcha",
        ]

    def validate_captcha(self, value):
        """Validate captcha input against stored captcha responses."""
        if not CaptchaStore.objects.filter(response=value).exists():
            raise exceptions.ValidationError("invalid captcha")
        return value

    def __init__(self, *args, **kwargs):
        """Initialize serializer and generate a new captcha."""
        super().__init__(*args, **kwargs)
        new_captcha = CaptchaStore.generate_key()
        self.fields["captcha"].help_text = (
            f'<img src="{captcha_image_url(new_captcha)}" alt="Captcha Image"/>'
        )
        self.captcha_key = new_captcha
