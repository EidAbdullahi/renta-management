from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tenant
from .forms import TenantForm  
from django.shortcuts import render, redirect
from .models import Payment
from .forms import PaymentForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment, Tenant
from .forms import PaymentForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Tenant, Payment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tenant, Payment
from django.contrib.auth.decorators import login_required


from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Payment, Tenant

def tenant_payments(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant)  # Get all payments for the tenant
    return render(request, 'users/tenant_payments.html', {'payments': payments, 'tenant': tenant})


def payment_list(request):
    payments = Payment.objects.all()  # Get all payments
    return render(request, 'users/payment_list.html', {'payments': payments})
def tenant_payments(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant)  # Get payments for this tenant
    return render(request, 'users/tenant_payments.html', {'payments': payments, 'tenant': tenant})

def some_view(request, tenant_id):
    return redirect(reverse('add_payment_tenant', args=[tenant_id]))

@login_required
# def add_payment(request, tenant_id):
#     tenant = get_object_or_404(Tenant, id=tenant_id)
#     if request.method == 'POST':
#         # Handle payment form submission
#         pass
#     return render(request, 'users/add_payment.html', {'tenant': tenant})
def add_payment(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = tenant  # ✅ Assign Tenant, not User
            payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'users/add_payment.html', {'form': form, 'tenant': tenant})


# def payment_list(request):
#     payments = Payment.objects.all().select_related('tenant')  # Optimize query
#     return render(request, 'users/payment_list.html', {'payments': payments})


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

def update_rent_status(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == "POST":
        rent_status = request.POST.get("rent_status")
        tenant.rent_amount_paid = True if rent_status == "Paid" else False
        tenant.save()
    return redirect("tenant_list")  # Redirect back to the tenant list