from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tenant
from .forms import TenantForm  

# Add Tenant
@login_required
def add_tenant(request):
    if request.method == "POST":
        form = TenantForm(request.POST, request.FILES)  # Ensure request.FILES for file handling
        if form.is_valid():
            form.save()
            return redirect('tenant_list')  # Redirect after saving
    else:
        form = TenantForm()
    
    return render(request, 'users/add_tenant.html', {'form': form})

# List Tenants
@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()  # Fetch all tenants
    return render(request, 'users/tenant_list.html', {'tenants': tenants})

# Edit Tenant Information
@login_required
def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=tenant)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'users/edit_tenant.html', {'form': form, 'tenant': tenant})

# Delete Tenant
@login_required
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'users/delete_tenant.html', {'tenant': tenant})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to dashboard after login

# User Logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page

# User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

# Dashboard View
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'users/dashboard.html')  # Ensure 'dashboard.html' exists
