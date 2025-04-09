from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tenant, Payment
from .models import Expense
from .forms import ExpenseForm
# forms.py
from django import forms
from .forms import TenantForm, PaymentForm
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Max
from django.shortcuts import render
from .models import Tenant, Property, Payment
from users.models import Payment, Tenant, Property
from django.db.models import Sum
from django.contrib import messages  # Import the messages module
from django.shortcuts import redirect
from users.models import Tenant, Employee, Payment  # Import Employee
from django.db.models import Sum
# ✅ List Payments (Optimized with select_related)
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
import calendar
import csv



from django.shortcuts import render
from .models import Employee  # Make sure this is imported
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm  # Assuming you have a form for Employee
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from django.template.loader import get_template
from django.shortcuts import render
from .models import Employee  # Import the Employee model



from django.shortcuts import render
from django.db.models import Q
from .models import Employee  # Assuming you have an Employee model


# Employeees views.
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')  # Redirect to employee list after deletion
    return render(request, 'users/confirm_delete.html', {'employee': employee})

def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee/edit_employee.html', {'form': form, 'employee': employee})


class EmployeeSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search by Name')
    position = forms.ChoiceField(
        required=False,
        choices=[('', 'Filter by Position'), 
                 ('Manager', 'Manager'), 
                 ('Developer', 'Developer'), 
                 ('Designer', 'cleaner')],
        label='Position'
    )

def employee_list(request):
    employees = Employee.objects.all()  # Fetch all employees from the database
    form = EmployeeSearchForm(request.GET)  # Get form data from the request

    if form.is_valid():
        search_term = form.cleaned_data.get('search')
        position_filter = form.cleaned_data.get('position')
        
        if search_term:
            employees = employees.filter(full_name__icontains=search_term)  # Case-insensitive search
        
        if position_filter:
            employees = employees.filter(position=position_filter)  # Filter by position
    
    return render(request, 'employee/employee_list.html', {'employees': employees})




def register_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employee/register_employee.html', {'form': form})








@login_required
def payment_list(request):
    # Get the latest payment per tenant
    latest_payments = Payment.objects.filter(
        id__in=Payment.objects.values('tenant').annotate(latest=Max('id')).values('latest')
    ).select_related('tenant')

    return render(request, 'tenant/payment_list.html', {'payments': latest_payments})


# ✅ View Payments for a Specific Tenant
@login_required
def tenant_payments(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant)
    return render(request, 'tenant/tenant_payments.html', {'payments': payments, 'tenant': tenant})

# ✅ Add Payment for Tenant (Handles Receipt Upload)
@login_required



@login_required
def add_payment(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = tenant
            payment.save()
            messages.success(request, "✅ Payment added successfully!")  # ✅ Success message
            return redirect('add_payment', tenant_id=tenant.id)  # Redirect to avoid form resubmission
    else:
        form = PaymentForm()
    return render(request, 'tenant/add_payment.html', {'form': form, 'tenant': tenant})




def payment_summary(request):
    month = request.GET.get('month')
    export = request.GET.get('export')

    if month:
        selected_month = int(month)
    else:
        selected_month = timezone.now().month

    payments = Payment.objects.filter(payment_date__month=selected_month)
    total_collected = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    paid_tenants = payments.filter(status='Paid')
    unpaid_tenants = Tenant.objects.exclude(
        id__in=paid_tenants.values_list('tenant_id', flat=True)
    )

    paid_count = paid_tenants.count()
    unpaid_count = unpaid_tenants.count()

    # CSV Export logic
    if export == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="payments_{selected_month}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Tenant', 'Amount', 'Date', 'Status'])
        for p in payments:
            writer.writerow([p.tenant.name, p.amount_paid, p.payment_date, p.status])
        return response

    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]

    context = {
    'month_choices': month_choices,
    'month_name': calendar.month_name[selected_month],  # ✅ This line
    
      }

    context = {
        'payments': payments,
        'paid_tenants': paid_tenants,
        'unpaid_tenants': unpaid_tenants,
        'selected_month': selected_month,
        'month_choices': month_choices,
        # 'month_name': month_name[selected_month],
        'total_collected': total_collected,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
    }
    return render(request, 'tenant/payment_summary.html', context)

def export_payments_csv(request):
    month = int(request.GET.get('month', timezone.now().month))
    payments = Payment.objects.filter(payment_date__month=month)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="payments_{month}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Tenant', 'Amount Paid', 'Date', 'Method', 'Status'])

    for payment in payments:
        writer.writerow([
            payment.tenant.name,
            payment.amount_paid,
            payment.payment_date,
            payment.payment_method,
            payment.status
        ])
    return response

@receiver(post_save, sender=Payment)
def update_payment_status(sender, instance, **kwargs):
    # Check if it's a new payment or an updated one
    instance.update_payment_status()

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
    return render(request, 'tenant/add_tenant.html', {'form': form})

# ✅ List All Tenants
@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenant/tenant_list.html', {'tenants': tenants})

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
    return render(request, 'tenant/edit_tenant.html', {'form': form, 'tenant': tenant})

# ✅ Delete Tenant
@login_required
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'tenant/delete_tenant.html', {'tenant': tenant})

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
    total_employees = Employee.objects.count()  # Add employee count
    pending_payments = Payment.objects.filter(status="Pending").count()
    total_paid = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_payment_list = Payment.objects.count()  # Example, count all payments

    # Fetch last 5 recent payments
    recent_payments = Payment.objects.order_by('-payment_date')[:5]

    context = {
        'total_tenants': total_tenants,
        'total_employees': total_employees,  # Add to context
        'pending_payments': pending_payments,
        'total_paid': total_paid,
        'recent_payments': recent_payments,
        'total_payment_list': total_payment_list,
    }

    return render(request, 'users/dashboard.html', context)



def generate_financial_report(month=None):
    if not month:
        month = timezone.now().month
    
    # Calculate Total Income
    total_income = Payment.objects.filter(payment_date__month=month).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    # Calculate Total Expenses
    total_expenses = Expense.objects.filter(expense_date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate Net Profit
    net_profit = total_income - total_expenses
    
    # Summary Information
    report_summary = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'month': timezone.now().strftime('%B'),
    }

    return report_summary

def financial_report(request):
    # Get the selected month from GET parameter or use current month
    month = request.GET.get('month')
    if month:
        selected_month = int(month)
    else:
        selected_month = timezone.now().month
    
    # Generate the financial report
    report_summary = generate_financial_report(month=selected_month)
    
    context = {
        'report_summary': report_summary,
        'selected_month': selected_month,
    }
    return render(request, 'tenant/financial_report.html', context)

def export_financial_report(request):
    month = request.GET.get('month')
    if not month:
        month = timezone.now().month

    report_summary = generate_financial_report(month=month)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{month}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Month', 'Total Income', 'Total Expenses', 'Net Profit'])
    writer.writerow([report_summary['month'], report_summary['total_income'], report_summary['total_expenses'], report_summary['net_profit']])

    return response


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # Redirect to a page showing all expenses
    else:
        form = ExpenseForm()

    return render(request, 'tenant/add_expense.html', {'form': form})



def expense_list(request):
    # Get the selected month or default to the current month
    month = request.GET.get('month', None)
    
    # Filter expenses by month if provided
    if month:
        expenses = Expense.objects.filter(expense_date__month=month)
    else:
        expenses = Expense.objects.all()
    
    # Calculate total expenses for the filtered data
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'month': month,
    }
    
    return render(request, 'tenant/expense_list.html', context)
