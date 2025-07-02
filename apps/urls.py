# apps/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('app/<int:app_id>/', views.app_detail, name='app_detail'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('supervisor/approve/<int:review_id>/', views.approve_review, name='approve_review'),
    path('supervisor/reject/<int:review_id>/', views.reject_review, name='reject_review'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]