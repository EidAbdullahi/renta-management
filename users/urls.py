from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from . import views  # Import views from your app

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),  # Redirect root to login
    path('login/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Ensure dashboard view exists
]
