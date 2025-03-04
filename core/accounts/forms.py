from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    capthca =  CaptchaField()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    captcha= CaptchaField()

    class Meta:
        model = User
        fields = ('email', 'password')

class CustomPasswordChangeForm(PasswordChangeForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = '__all__'