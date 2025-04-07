from django import forms
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for submitting a comment with CAPTCHA verification."""

    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = (
            "name",
            "email",
            "subject",
            "message",
            "recommend",
        )
