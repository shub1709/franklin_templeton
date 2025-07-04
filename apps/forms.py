from django import forms
from .models import UserReview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=UserReview.RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Rating"
    )
    class Meta:
        model = UserReview
        fields = ['review_text', 'sentiment', 'rating']
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
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2']

#     def clean(self):
#         cleaned_data = super().clean()

#         # ✅ Suppress password-related errors if username is invalid
#         if 'username' in self.errors:
#             # Remove all password-related errors
#             for field in ['password1', 'password2']:
#                 if field in self._errors:
#                     del self._errors[field]

#         return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def is_valid(self):
        """
        Override is_valid to prevent password validation if username is invalid.
        """
        super_valid = super().is_valid()

        # If username is invalid, strip password-related errors
        if 'username' in self.errors:
            for field in ['password1', 'password2']:
                if field in self.errors:
                    del self.errors[field]

        # Recompute validity based on modified errors
        return not self.errors
