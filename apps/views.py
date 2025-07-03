from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import GooglePlayApp, UserReview, ExistingReview
from .forms import ReviewForm
# from .search_utils import search_engine
from .search_utils import get_search_engine


def home(request):
    query = request.GET.get('q', '').strip()
    apps = []
    main_app = None
    similar_apps = []

    if query:
        results = get_search_engine().search(query, max_results=50)
        if results:
            main_app = results[0]
            similar_apps = [app for app in results[1:] if app.category == main_app.category][:20]

    context = {
        'query': query,
        'main_app': main_app,
        'similar_apps': similar_apps,
        'show_results': bool(query)
    }
    return render(request, 'apps/home.html', context)

def autocomplete(request):
    """API endpoint for autocomplete suggestions"""
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if len(query) >= 3:
        # suggestions = get_search_engine().get_suggestions(query, max_suggestions=10)
        suggestions = get_search_engine().get_suggestions(query, max_suggestions=10000)
    
    return JsonResponse({'suggestions': suggestions})

def app_detail(request, app_id):
    """App detail page with reviews"""
    app = get_object_or_404(GooglePlayApp, id=app_id)
    existing_reviews = app.existing_reviews.all()
    user_reviews = app.user_reviews.filter(status='approved')
    
    # Handle new review submission
    review_form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.app = app
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted for approval!')
            return redirect('app_detail', app_id=app.id)
    
    context = {
        'app': app,
        'existing_reviews': existing_reviews,
        'user_reviews': user_reviews,
        'review_form': review_form,
    }
    return render(request, 'apps/app_detail.html', context)

# def is_supervisor(user):
#     """Check if user is a supervisor (staff member)"""
#     return user.is_staff

def is_supervisor(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_supervisor)
def supervisor_dashboard(request):
    """Dashboard for supervisors to manage reviews"""
    pending_reviews = UserReview.objects.filter(status='pending').order_by('-created_at')
    
    context = {
        'pending_reviews': pending_reviews,
    }
    return render(request, 'apps/supervisor_dashboard.html', context)

@login_required
@user_passes_test(is_supervisor)
def approve_review(request, review_id):
    """Approve a review"""
    review = get_object_or_404(UserReview, id=review_id)
    review.status = 'approved'
    review.approved_by = request.user
    review.approved_at = timezone.now()
    review.save()
    
    messages.success(request, f'Review for "{review.app.app_name}" has been approved!')
    return redirect('supervisor_dashboard')

@login_required
@user_passes_test(is_supervisor)
def reject_review(request, review_id):
    """Reject a review"""
    review = get_object_or_404(UserReview, id=review_id)
    review.status = 'rejected'
    review.approved_by = request.user
    review.approved_at = timezone.now()
    review.save()
    
    messages.success(request, f'Review for "{review.app.app_name}" has been rejected!')
    return redirect('supervisor_dashboard')

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
