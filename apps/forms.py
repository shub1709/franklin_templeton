from django import forms
from .models import UserReview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['review_text', 'sentiment']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
            'sentiment': forms.Select(attrs={
                'class': 'form-control'
            })
        }

# Added this class to throw the error while registering a new account which already exists
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()

        # Suppress password mismatch if username was invalid
        if self.errors.get('username') and self.errors.get('password2'):
            password2_errors = self.errors.get('password2')
            if password2_errors and "didn't match" in password2_errors[0]:
                del self.errors['password2']

        return cleaned_data
