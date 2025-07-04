from django import forms
from .models import UserReview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

    def clean(self):
        cleaned_data = super().clean()

        # Remove "password2 mismatch" error if username error exists
        if 'username' in self.errors and 'password2' in self.errors:
            password2_errors = self.errors.get('password2')
            if password2_errors and "didn't match" in password2_errors[0]:
                del self.errors['password2']

        return cleaned_data
