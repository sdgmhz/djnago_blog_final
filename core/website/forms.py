from django import forms
from captcha.fields import CaptchaField

from .models import Contact


class ContactForm(forms.ModelForm):
    """Form for user contact submissions with captcha verification."""

    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = (
            "name",
            "email",
            "subject",
            "message",
            "captcha",
        )
