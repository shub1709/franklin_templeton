from django.contrib import admin
from .models import GooglePlayApp, UserReview, ExistingReview

@admin.register(GooglePlayApp)
class GooglePlayAppAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'category', 'rating', 'reviews_count', 'installs']
    list_filter = ['category', 'content_rating', 'app_type']
    search_fields = ['app_name', 'category', 'genres']

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['app', 'user', 'sentiment', 'status', 'created_at']
    list_filter = ['status', 'sentiment', 'created_at']
    search_fields = ['app__app_name', 'user__username', 'review_text']

@admin.register(ExistingReview)
class ExistingReviewAdmin(admin.ModelAdmin):
    list_display = ['app', 'sentiment', 'sentiment_polarity']
    list_filter = ['sentiment']
    search_fields = ['app__app_name', 'review_text']