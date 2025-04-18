from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tenant, Payment
from .models import Expense
from .forms import ExpenseForm
from django.utils.timezone import now
# forms.py
from django import forms
from .forms import TenantForm, PaymentForm
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Max
from django.shortcuts import render
from .models import Tenant, Property, Payment
from users.models import Payment, Tenant, Property
from .forms import PropertyForm
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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404, redirect
from .models import Expense


from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from .forms import PaymentForm  # Create a form for editing payments

# View for editing a payment
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # If the request method is POST, we are processing the form submission
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()  # Save the updated payment record
            return redirect('payment_list')  # Redirect to the list page after saving
    else:
        # If the request method is GET, just display the form with existing payment data
        form = PaymentForm(instance=payment)

    return render(request, 'tenant/edit_payment.html', {'form': form, 'payment': payment})

# View for deleting a payment
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':  # Only delete on POST request to avoid accidental deletions
        payment.delete()  # Delete the payment record
        return redirect('payment_list')  # Redirect to the payment list page after deletion

    return render(request, 'tenant/confirm_delete.html', {'payment': payment})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('expense_list')  # Redirect to the expense list after deletion


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # Redirect to the expense list after editing
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})


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



# from django.shortcuts import render
# from django.utils import timezone
# from django.db.models import Sum
# from django.http import HttpResponse
# import csv, calendar
# from .models import Payment, Tenant  # Adjust import paths as needed

from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render
from .models import Tenant, Payment
import calendar

def payment_summary(request):
    # Get selected month and year from GET request
    today = datetime.today()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))
    month_name = calendar.month_name[selected_month]

    # Get all tenants
    all_tenants = Tenant.objects.all()

    # Get paid tenants for selected month/year
    paid_payments = Payment.objects.filter(
        payment_date__year=selected_year,
        payment_date__month=selected_month,
        status='Paid'
    )

    paid_tenants = paid_payments.select_related('tenant')
    paid_tenant_ids = paid_tenants.values_list('tenant_id', flat=True)

    # Unpaid tenants: all not in the list of paid IDs
    unpaid_tenants = all_tenants.exclude(id__in=paid_tenant_ids)

    # Total rent expected: sum of rent from all tenants
    expected_total = all_tenants.aggregate(total=Sum('rent_amount'))['total'] or 0

    # Total collected
    total_collected = paid_payments.aggregate(total=Sum('amount_paid'))['total'] or 0

    # Monthly trend (for bar chart - latest 6 months)
    from django.db.models.functions import TruncMonth
    recent_payments = Payment.objects.filter(status='Paid')
    recent_months = recent_payments.annotate(month=TruncMonth('payment_date')).values('month').annotate(total=Sum('amount_paid')).order_by('-month')[:6]

    monthly_labels = [p['month'].strftime('%b') for p in reversed(recent_months)]
    monthly_data = [p['total'] for p in reversed(recent_months)]

    context = {
        'month_choices': [(i, calendar.month_name[i]) for i in range(1, 13)],
        'year_choices': list(range(today.year - 2, today.year + 2)),
        'selected_month': selected_month,
        'selected_year': selected_year,
        'month_name': month_name,

        'paid_tenants': paid_tenants,
        'unpaid_tenants': unpaid_tenants,
        'paid_count': paid_tenants.count(),
        'unpaid_count': unpaid_tenants.count(),
        'total_collected': total_collected,
        'expected_total': expected_total,

        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
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
        'now': now()
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




def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property/propert_list.html', {'properties': properties})

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'property/add_property.html', {'form': form})
