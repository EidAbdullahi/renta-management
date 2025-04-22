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
from freelancers.models import Freelancer
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
from .forms import ProfileUpdateForm





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

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import csv
from django.shortcuts import render
from .models import VacantRoom
from .forms import VacantRoomForm, VacancySearchForm
# Assuming the generate_financial_report function is defined elsewhere
from .utils import generate_financial_report
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserRegisterForm
from .forms import EmployeeSearchForm
from django.core.paginator import Paginator
import csv
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from .models import Tenant, Payment
import calendar


# views.py
# views.py
@login_required
def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, '✅ Your profile has been updated.')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'p_form': p_form})


def is_superuser(user):
    return user.is_superuser

@login_required
# @user_passes_test(is_superuser)
def add_vacancy(request):
    if request.method == 'POST':
        form = VacantRoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vacancy_list')
    else:
        form = VacantRoomForm()
    return render(request, 'users/add_vacancy.html', {'form': form})



def vacancy_list(request):
    form = VacancySearchForm(request.GET)
    rooms = VacantRoom.objects.filter(is_available=True)
    freelancers = Freelancer.objects.all()

    # Filtering based on search form
    if form.is_valid():
        query = form.cleaned_data.get('query')
        room_type = form.cleaned_data.get('room_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')

        if query:
            rooms = rooms.filter(Q(title__icontains=query) | Q(location__icontains=query))
        if room_type:
            rooms = rooms.filter(room_type=room_type)
        if min_price is not None:
            rooms = rooms.filter(amount__gte=min_price)
        if max_price is not None:
            rooms = rooms.filter(amount__lte=max_price)
        if location:
            rooms = rooms.filter(Q(location__icontains=location))  # Filter based on location
           
    # Pagination (after filtering)
    paginator = Paginator(rooms, 6)
    page = request.GET.get('page')
    rooms = paginator.get_page(page)

    # Latest and Popular rooms (assuming views added later)
    latest_rooms = VacantRoom.objects.order_by('-created_at')[:6]
    popular_rooms = VacantRoom.objects.order_by('-created_at')[:6]  # Replace with '-views' when views field is added

    return render(request, 'users/vacancy_list.html', {
        'rooms': rooms,
        'form': form,
        'latest_rooms': latest_rooms,
        'popular_rooms': popular_rooms,
        'freelancers': freelancers, 
    })

def vacancy_detail(request, slug):
    room = get_object_or_404(VacantRoom, slug=slug)
    return render(request, 'users/vacancy_details.html', {'room': room})


# View for editing a payment
@login_required
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = payment.tenant  # Reassign same tenant
            payment.save()
            return redirect('payment_list')
        else:
            print("Form Errors:", form.errors)
    else:
        form = PaymentForm(instance=payment)

    return render(request, 'tenant/edit_payment.html', {'form': form, 'payment': payment})


# View for deleting a payment
@login_required
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
@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')  # Redirect to employee list after deletion
    return render(request, 'users/confirm_delete.html', {'employee': employee})

@login_required
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




@login_required
def employee_list(request):
    # Filter employees by the logged-in user
    employees = Employee.objects.filter(user=request.user)  # Only show employees related to the logged-in user
    
    # Initialize the search form with GET data
    form = EmployeeSearchForm(request.GET)
    
    # Check if the form is valid
    if form.is_valid():
        search_term = form.cleaned_data.get('search')
        position_filter = form.cleaned_data.get('position')
        
        # Apply search filters
        if search_term:
            employees = employees.filter(full_name__icontains=search_term)  # Case-insensitive search
        
        if position_filter:
            employees = employees.filter(position=position_filter)  # Filter by position
    
    # Render the template with the filtered employee list and form
    return render(request, 'employee/employee_list.html', {'employees': employees, 'form': form})


@login_required
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        employee = form.save(commit=False)
        employee.user = request.user
            # Now save the employee with the user
        employee.save()
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





@login_required
def add_payment(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)  # Don't save yet
            payment.user = request.user  # Set the logged-in user
            payment.tenant = tenant
            payment.save()
            messages.success(request, "✅ Payment added successfully!")  # ✅ Success message
            return redirect('add_payment', tenant_id=tenant.id)  # Redirect to avoid form resubmission
    else:
        form = PaymentForm()
    return render(request, 'tenant/add_payment.html', {'form': form, 'tenant': tenant})




from datetime import datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
import csv
from .models import Tenant, Payment

@login_required
def payment_summary(request):
    today = datetime.today()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))
    month_name = calendar.month_name[selected_month]

    # ✅ Filter tenants registered on or before the selected month/year
    last_day = calendar.monthrange(selected_year, selected_month)[1]
    cutoff_date = date(selected_year, selected_month, last_day)

    all_tenants = Tenant.objects.filter(user=request.user, move_in_date__lte=cutoff_date)

    paid_payments = Payment.objects.filter(
        payment_date__year=selected_year,
        payment_date__month=selected_month,
        status='Paid'
    )

    paid_tenants = paid_payments.select_related('tenant')
    paid_tenant_ids = paid_tenants.values_list('tenant_id', flat=True)
    unpaid_tenants = all_tenants.exclude(id__in=paid_tenant_ids)

    expected_total = all_tenants.aggregate(total=Sum('rent_amount'))['total'] or 0
    total_collected = paid_payments.aggregate(total=Sum('amount_paid'))['total'] or 0

    from django.db.models.functions import TruncMonth
    recent_payments = Payment.objects.filter(status='Paid')
    recent_months = recent_payments.annotate(month=TruncMonth('payment_date')) \
        .values('month').annotate(total=Sum('amount_paid')).order_by('-month')[:6]

    monthly_labels = [p['month'].strftime('%b') for p in reversed(recent_months)]
    monthly_data = [p['total'] for p in reversed(recent_months)]

    # ✅ Excel export with both paid and unpaid tenants
    if request.GET.get('export') == 'excel':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="payment_summary_{selected_month}_{selected_year}.csv"'

        writer = csv.writer(response)

        # --- Paid Section ---
        writer.writerow(['Paid Tenants'])
        writer.writerow(['Tenant Name', 'Phone', 'Unit Number', 'Amount Paid', 'Payment Date', 'Payment Method', 'Status'])

        for payment in paid_tenants:
            writer.writerow([
                payment.tenant.name,
                payment.tenant.phone,
                payment.tenant.unit_number,
                payment.amount_paid,
                payment.payment_date,
                payment.payment_method,
                payment.status
            ])

        writer.writerow([])  # Empty row for separation

        # --- Unpaid Section ---
        writer.writerow(['Unpaid Tenants'])
        writer.writerow(['Tenant Name', 'Phone', 'Unit Number', 'Email'])

        for tenant in unpaid_tenants:
            writer.writerow([
                tenant.name,
                tenant.phone,
                tenant.unit_number,
                tenant.email
            ])

        return response

    # Normal page render
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



@login_required
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

@login_required
@receiver(post_save, sender=Payment)
def update_payment_status(sender, instance, **kwargs):
    # Check if it's a new payment or an updated one
    instance.update_payment_status()

# ✅ Add New Tenant
@login_required
def add_tenant(request):
    if request.method == "POST":
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid(): tenant = form.save(commit=False)
        tenant.user = request.user  # ✅ Link the current logged-in user
        tenant.save()
        return redirect('tenant_list')

            
    else:
        form = TenantForm()
    return render(request, 'tenant/add_tenant.html', {'form': form})

# ✅ List All Tenants
@login_required
def tenant_list(request):
    tenants = Tenant.objects.filter(user=request.user)
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
    return render(request, 'formtenant/delete_tenant.html', {'tenant': tenant})

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







@login_required
def dashboard(request):
    # Get the current user
    current_user = request.user

    # Get all tenants for the current user
    total_tenants = Tenant.objects.filter(user=current_user).count()
    total_employees = Employee.objects.filter(user=current_user).count()  # Add employee count
    pending_payments = Payment.objects.filter(user=current_user, status="Pending").count()
    total_paid = Payment.objects.filter(user=current_user).aggregate(total=Sum('amount_paid'))['total'] or 0
    total_payment_list = Payment.objects.filter(user=current_user).count()  # Example, count all payments

    # Fetch last 5 recent payments for the current user
    recent_payments = Payment.objects.filter(user=current_user).order_by('-payment_date')[:5]

    # Calculate total occupied and available units for the current user
    properties = Property.objects.filter(user=current_user)
    total_occupied_units = sum([p.occupied_units for p in properties])
    total_available_units = sum([p.available_units for p in properties])

    # Prepare the data to display for the current user
    context = {
        'total_tenants': total_tenants,
        'total_employees': total_employees,
        'pending_payments': pending_payments,
        'total_paid': total_paid,
        'recent_payments': recent_payments,
        'total_payment_list': total_payment_list,
        'total_occupied_units': total_occupied_units,
        'total_available_units': total_available_units,
        'now': datetime.now(),
        'user': current_user,  # Include user information
    }

    return render(request, 'users/dashboard.html', context)




@login_required
def financial_report(request):
    # Get the selected month from GET parameter or use current month
    month = request.GET.get('month')
    if month:
        try:
            selected_month = int(month)
        except ValueError:
            selected_month = timezone.now().month
    else:
        selected_month = timezone.now().month

    # Now pass the correct month to the report function
    # In your view or wherever you call the function
    report_summary = generate_financial_report(request, month=selected_month)


    import calendar
    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]

    context = {
        'report_summary': report_summary,
        'selected_month': selected_month,
        'month_choices': month_choices,
    }
    return render(request, 'tenant/financial_report.html', context)

@login_required
def export_financial_report(request):
    # Get the selected month from GET parameter or use current month
    month = request.GET.get('month')
    if not month:
        month = timezone.now().month

    report_summary = generate_financial_report(month=month)
    
    # Prepare the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{month}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Month', 'Total Income', 'Total Expenses', 'Net Profit'])
    writer.writerow([report_summary['month'], report_summary['total_income'], report_summary['total_expenses'], report_summary['net_profit']])

    return response


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)  # Don't save yet
            expense.user = request.user  # Set the logged-in user
            expense.save()  # Now save the expense
            return redirect('expense_list')  # Redirect to a page showing all expenses
    else:
        form = ExpenseForm()

    return render(request, 'tenant/add_expense.html', {'form': form})


@login_required



def expense_list(request):
    # Get the selected month from GET parameters or default to None (all months)
    month = request.GET.get('month', None)
    
    # If a month is selected, filter by that month; otherwise, show all expenses for the current user
    if month:
        expenses = Expense.objects.filter(expense_date__month=month, user=request.user)  # Filter by month and user
    else:
        expenses = Expense.objects.filter(user=request.user)  # Show all expenses for the user if no month is selected

    # Calculate the total expenses for the filtered data
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'month': month,
        'months': [
            ("01", "January"),
            ("02", "February"),
            ("03", "March"),
            ("04", "April"),
            ("05", "May"),
            ("06", "June"),
            ("07", "July"),
            ("08", "August"),
            ("09", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
    }
    
    return render(request, 'tenant/expense_list.html', context)


@login_required
def property_list(request):
    properties = Property.objects.filter(user=request.user)
    return render(request, 'property/propert_list.html', {'properties': properties})


@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user  # ✅ Assign the current user
            property.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'property/add_property.html', {'form': form})


# views.py
@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('property_list')  # Make sure this is your correct URL name
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'property/edit_property.html', {'form': form, 'property': property_obj})

@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return redirect('property_list')
