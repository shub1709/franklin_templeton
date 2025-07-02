# apps/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class GooglePlayApp(models.Model):
    app_name = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    rating = models.FloatField(null=True, blank=True)
    reviews_count = models.IntegerField(default=0)
    size = models.CharField(max_length=50)
    installs = models.CharField(max_length=50)
    app_type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    content_rating = models.CharField(max_length=50)
    genres = models.CharField(max_length=200)
    last_updated = models.CharField(max_length=50)
    current_version = models.CharField(max_length=50)
    android_version = models.CharField(max_length=50)
    
    def __str__(self):
        return self.app_name
    
    class Meta:
        ordering = ['-rating', '-reviews_count']

class UserReview(models.Model):
    SENTIMENT_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Neutral', 'Neutral'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    app = models.ForeignKey(GooglePlayApp, on_delete=models.CASCADE, related_name='user_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='Neutral')
    sentiment_polarity = models.FloatField(default=0.0)
    sentiment_subjectivity = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_reviews')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.app.app_name} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']

class ExistingReview(models.Model):
    app = models.ForeignKey(GooglePlayApp, on_delete=models.CASCADE, related_name='existing_reviews')
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20, default='Neutral')
    sentiment_polarity = models.FloatField(default=0.0)
    sentiment_subjectivity = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.app.app_name} - Review"