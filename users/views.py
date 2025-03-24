from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Tenant
from .forms import TenantForm  # You'll create this form soon
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import TenantForm  # Import the form you've created


def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            # Redirect to a success page or back to the list of tenants
            return redirect('tenant_list')  # Change 'tenant_list' to your desired URL name
    else:
        form = TenantForm()
    
    return render(request, 'users/add_tenant.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

#from django.shortcuts import render

def tenant_list(request):
    tenants = Tenant.objects.all()  # Make sure you fetch the tenants
    return render(request, 'users/tenant_list.html', {'tenants': tenants})


# views.py

def add_tenant(request):
    if request.method == "POST":
        form = TenantForm(request.POST, request.FILES)  # Include request.FILES for file handling
        if form.is_valid():
            form.save()
            return redirect('tenant_list')  # Redirect after successful submission
    else:
        form = TenantForm()
    
    return render(request, 'tenants/add_tenant.html', {'form': form})


def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or do something after saving
    else:
        form = TenantForm()
    
    return render(request, 'users/add_tenant.html', {'form': form})

# Edit tenant information
@login_required
def edit_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'edit_tenant.html', {'form': form})

# Delete a tenant
@login_required
def delete_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'delete_tenant.html', {'tenant': tenant})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to dashboard after login

@login_required(login_url='/login/')  # Redirect to login if not authenticated
def dashboard(request):
    return render(request, 'users/dashboard.html')  # Create 'dashboard.html'

