from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tenant, Payment
from .forms import TenantForm, PaymentForm
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Max
from django.shortcuts import render
from .models import Tenant, Property, Payment
from django.shortcuts import render
from users.models import Payment, Tenant, Property
from django.db.models import Sum
# ✅ List Payments (Optimized with select_related)


@login_required
def payment_list(request):
    # Get the latest payment per tenant
    latest_payments = Payment.objects.filter(
        id__in=Payment.objects.values('tenant').annotate(latest=Max('id')).values('latest')
    ).select_related('tenant')

    return render(request, 'users/payment_list.html', {'payments': latest_payments})


# ✅ View Payments for a Specific Tenant
@login_required
def tenant_payments(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant)
    return render(request, 'users/tenant_payments.html', {'payments': payments, 'tenant': tenant})

# ✅ Add Payment for Tenant (Handles Receipt Upload)
@login_required
def add_payment(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)  # ✅ Ensure request.FILES is included
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = tenant
            payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'users/add_payment.html', {'form': form, 'tenant': tenant})

# ✅ Add New Tenant
@login_required
def add_tenant(request):
    if request.method == "POST":
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'users/add_tenant.html', {'form': form})

# ✅ List All Tenants
@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'users/tenant_list.html', {'tenants': tenants})

# ✅ Edit Tenant Details
@login_required
def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'users/edit_tenant.html', {'form': form, 'tenant': tenant})

# ✅ Delete Tenant
@login_required
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'users/delete_tenant.html', {'tenant': tenant})

# ✅ Update Tenant Rent Payment Status
@login_required
def update_rent_status(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == "POST":
        rent_status = request.POST.get("rent_status")
        tenant.rent_amount_paid = True if rent_status == "Paid" else False
        tenant.save()
    return redirect("tenant_list")

# ✅ Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# ✅ Dashboard




def dashboard(request):
    total_tenants = Tenant.objects.count()
    total_properties = Property.objects.count()
    pending_payments = Payment.objects.filter(status="Pending").count()
    total_paid = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0

    # Fetch last 5 recent payments
    recent_payments = Payment.objects.order_by('-payment_date')[:5]

    context = {
        'total_tenants': total_tenants,
        'total_properties': total_properties,
        'pending_payments': pending_payments,
        'total_paid': total_paid,
        'recent_payments': recent_payments,  # Make sure this is passed
    }
    

    return render(request, 'users/dashboard.html', context)
