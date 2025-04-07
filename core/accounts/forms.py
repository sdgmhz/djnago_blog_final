from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with captcha."""

    capthca = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "password")


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = "__all__"


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = "__all__"


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = "__all__"
