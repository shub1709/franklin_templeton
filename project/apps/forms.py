from django import forms
from .models import UserReview

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