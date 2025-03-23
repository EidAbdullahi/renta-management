from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to dashboard after login

@login_required(login_url='/login/')  # Redirect to login if not authenticated
def dashboard(request):
    return render(request, 'users/dashboard.html')  # Create 'dashboard.html'
