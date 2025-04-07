from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """Form for creating or updating a Category model instance"""

    class Meta:
        model = Category
        fields = ["name"]
