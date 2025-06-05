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
from .models import ForSaleProperty
from .forms import ForSalePropertyForm
from django.http import Http404
import json
from django.http import HttpResponse
from .utils import generate_invoice_pdf
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
from .forms import ProfileUpdateForm

import urllib.parse
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .forms import VacancySearchForm  # assuming you have this form



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
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Tenant, Payment

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from datetime import datetime, date


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
from .models import CommercialProperty
from .forms import CommercialPropertyForm


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
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render
from .models import Tenant, Payment
from .models import Partner
from .forms import PartnerForm

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Payment, Expense  # Adjust the import path if needed
import calendar
from django.shortcuts import render, redirect
from .forms import FreelancerContactForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Reaction
from .forms import ItemForm
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Q
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Transaction
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
import csv
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render
from .models import Transaction

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum
from collections import defaultdict
from .models import Transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# from .models import Sale
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def admin_sales_report(request):
    users = User.objects.all()
    transactions = Transaction.objects.select_related('user').order_by('-date')

    # Group totals by user
    user_totals = (
        Transaction.objects.values('user__username')
        .annotate(total_amount=Sum('amount'))
        .order_by('-total_amount')
    )

    context = {
        'transactions': transactions,
        'user_totals': user_totals,
    }
    return render(request, 'users/admin_sales_report.html', context)



@staff_member_required
def register_sale(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        item_title = request.POST.get('item_title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')

        Transaction.objects.create(
            user_id=user_id,
            category=category,
            item_title=item_title,
            amount=amount
        )
        return redirect('register_sale')

    return render(request, 'users/admin_register_sale.html', {'users': users})


@login_required
def user_sales_dashboard(request):
    sales = Transaction.objects.filter(user=request.user)
    total_sales = sales.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'users/user_sales.html', {
        'sales': sales,
        'total_sales': total_sales,
        'number_of_sales': sales.count()
    })


@login_required
def export_sales_csv(request):
    sales = Transaction.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename='sales_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv'"
    writer = csv.writer(response)
    writer.writerow(['Item Title', 'Category', 'Amount', 'Date'])
    for sale in sales:
        writer.writerow([sale.item_title, sale.get_category_display(), sale.amount, sale.date.strftime('%Y-%m-%d')])
    return response

def discover_items(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')

    items = Item.objects.all()

    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        items = items.filter(category=category)
    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)

    # Annotate like and love counts for all items (no matter sorting)
    items = items.annotate(
        like_count=Count('reactions', filter=Q(reactions__reaction_type='like')),
        love_count=Count('reactions', filter=Q(reactions__reaction_type='love')),
    )

    if sort == 'liked':
        items = items.order_by('-like_count')
    elif sort == 'loved':
        items = items.order_by('-love_count')
    else:
        items = items.order_by('-posted_at')

    return render(request, 'users/discover.html', {
        'items': items,
        'query': query,
        'category': category,
        'min_price': min_price,
        'max_price': max_price
    })


@login_required
def upload_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('discover')
    else:
        form = ItemForm()
    return render(request, 'users/upload.html', {'form': form})

def react_to_item(request, item_id, reaction_type):
    item = get_object_or_404(Item, id=item_id)
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    # Prevent duplicate reaction
    if not Reaction.objects.filter(item=item, session_id=session_id, reaction_type=reaction_type).exists():
        Reaction.objects.create(item=item, session_id=session_id, reaction_type=reaction_type)
    return redirect('discover')

@login_required
def preview_invoice(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'tenant/invoice_preview.html', {'payment': payment})

def contact_us(request):
    if request.method == 'POST':
        form = FreelancerContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'freelancers/contact_success.html')
    else:
        form = FreelancerContactForm()
    return render(request, 'freelancers/contact_form.html', {'form': form})

# views.py
# views.py

def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Account created successfully! Your account is pending approval by the admin..')
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
            return redirect('dashboard')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'p_form': p_form})


def is_superuser(user):
    return user.is_superuser

@login_required
# @user_passes_test(is_superuser)
@login_required  # Ensure that only logged-in users can access this view
def add_vacancy(request):
    if request.method == 'POST':
        form = VacantRoomForm(request.POST, request.FILES)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.user = request.user  # Automatically set the logged-in user
            vacancy.save()
            return redirect('vacancy_list')
    else:
        form = VacantRoomForm()

    return render(request, 'users/add_vacancy.html', {'form': form})



def vacancy_list(request):
    form = VacancySearchForm(request.GET)
    rooms = VacantRoom.objects.filter(is_available=True).order_by('-created_at')  # Order latest first
    freelancers = Freelancer.objects.all()
    partners = Partner.objects.all()

    # --- Search history management ---
    if 'search_history' not in request.session:
        request.session['search_history'] = []

    location = request.GET.get('location', request.session.get('location', ''))

    if location and location not in request.session['search_history']:
        request.session['search_history'].insert(0, location)
        if len(request.session['search_history']) > 5:
            request.session['search_history'].pop()
        request.session.modified = True

    # --- Filter form processing ---
    if form.is_valid():
        query = form.cleaned_data.get('query')
        room_type = form.cleaned_data.get('room_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if query:
            rooms = rooms.filter(Q(title__icontains=query) | Q(location__icontains=query))
        if location:
            rooms = rooms.filter(location__icontains=location)
        if room_type:
            rooms = rooms.filter(room_type=room_type)
        if min_price is not None:
            rooms = rooms.filter(amount__gte=min_price)
        if max_price is not None:
            rooms = rooms.filter(amount__lte=max_price)

    # --- One room per user if no filters/search applied ---
    is_filtered = any([
        request.GET.get('query'),
        request.GET.get('location'),
        request.GET.get('room_type'),
        request.GET.get('min_price'),
        request.GET.get('max_price'),
    ])

    if not is_filtered:
        unique_user_rooms = {}
        for room in rooms:
            if room.user_id not in unique_user_rooms:
                unique_user_rooms[room.user_id] = room  # Keep the latest room for each user
        rooms = list(unique_user_rooms.values())
    else:
        rooms = list(rooms)

    # --- WhatsApp message generation ---
    for room in rooms:
        if room.picture1:
            room.picture1_url = request.build_absolute_uri(room.picture1.url)
        else:
            room.picture1_url = ""

        short_desc = room.description.replace('\n', ' ').replace('\r', '')[:100]
        message = (
            f"Hello, I'm interested in \"{room.title}\" located in {room.location}. "
            f"Description: {short_desc}. "
            f"Photo: {room.picture1_url}"
        )
        room.whatsapp_message_url = "https://wa.me/254798883849?text=" + urllib.parse.quote(message)

    # --- Pagination ---
    paginator = Paginator(rooms, 12)
    page = request.GET.get('page')
    rooms = paginator.get_page(page)

    latest_rooms = VacantRoom.objects.order_by('-created_at')[:6]
    popular_rooms = VacantRoom.objects.order_by('-created_at')[:6]

    context = {
        'rooms': rooms,
        'form': form,
        'latest_rooms': latest_rooms,
        'popular_rooms': popular_rooms,
        'freelancers': freelancers,
        'partners': partners,
        'search_history': request.session.get('search_history', []),
        'location': location,
    }

    return render(request, 'users/vacancy_list.html', context)


@login_required
def home(request):
    return render(request, 'users/home.html')

def remove_location(request):
    location = request.GET.get('location')
    if location and 'search_history' in request.session:
        search_history = request.session['search_history']
        if location in search_history:
            search_history.remove(location)
            request.session['search_history'] = search_history
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)



from urllib.parse import quote

def vacancy_detail(request, slug):
    room = get_object_or_404(VacantRoom, slug=slug)
    partners = Partner.objects.all()

    # WhatsApp message setup
    message = f"Hello, I'm interested in the room '{room.title}' located at {room.location}. Is it still available?"
    phone_number = "0798883849"
    whatsapp_url = f"https://wa.me/{phone_number}?text={quote(message)}"

    # Get other rooms by the same user
    other_rooms = VacantRoom.objects.filter(user=room.user, is_available=True).exclude(id=room.id)

    context = {
        'room': room,
        'partners': partners,
        'whatsapp_url': whatsapp_url,
        'other_rooms': other_rooms,
    }
    return render(request, 'users/vacancy_details.html', context)



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
    
    return render(request, 'tenant/edit_expense.html', {'form': form, 'expense': expense})


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
    # Get latest payment per tenant belonging to the current user
    user_tenants = Tenant.objects.filter(user=request.user)
    
    latest_payment_ids = Payment.objects.filter(
        tenant__in=user_tenants
    ).values('tenant').annotate(latest=Max('id')).values_list('latest', flat=True)

    latest_payments = Payment.objects.filter(id__in=latest_payment_ids).select_related('tenant')

    return render(request, 'tenant/payment_list.html', {'payments': latest_payments})



# ✅ View Payments for a Specific Tenant
@login_required
def tenant_payments(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)

    # 🔐 Ensure the tenant belongs to the logged-in user
    if tenant.user != request.user:
        raise Http404("You do not have permission to view this tenant's payments.")

    payments = Payment.objects.filter(tenant=tenant)

    return render(request, 'tenant/tenant_payments.html', {
        'payments': payments,
        'tenant': tenant
    })

@login_required
def add_payment(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id, user=request.user)
    payment = None

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.tenant = tenant
            payment.save()

            messages.success(request, "✅ Payment added successfully!")
            # Instead of redirect, fall through to render same page with payment info
    else:
        form = PaymentForm(user=request.user)

    return render(request, 'tenant/add_payment.html', {
        'form': form,
        'tenant': tenant,
        'payment': payment,  # This will be None on GET, or payment object on successful POST
    })




@login_required
def download_invoice_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    pdf = generate_invoice_pdf(payment)
    if not pdf:
        return HttpResponse("Error generating PDF", status=500)

    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'
    return response

@login_required
def payment_summary(request):
    today = datetime.today()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))
    month_name = calendar.month_name[selected_month]
    user = request.user  # Current logged-in user

    # ✅ Only include tenants of the logged-in user
    last_day = calendar.monthrange(selected_year, selected_month)[1]
    cutoff_date = date(selected_year, selected_month, last_day)

    all_tenants = Tenant.objects.filter(user=user, move_in_date__lte=cutoff_date)

    # ✅ Only include payments of the logged-in user's tenants
    paid_payments = Payment.objects.filter(
        payment_date__year=selected_year,
        payment_date__month=selected_month,
        status='Paid',
        tenant__user=user  # Ensures tenant belongs to the logged-in user
    )

    paid_tenants = paid_payments.select_related('tenant')
    paid_tenant_ids = paid_tenants.values_list('tenant_id', flat=True)
    unpaid_tenants = all_tenants.exclude(id__in=paid_tenant_ids)

    expected_total = all_tenants.aggregate(total=Sum('rent_amount'))['total'] or 0
    total_collected = paid_payments.aggregate(total=Sum('amount_paid'))['total'] or 0

    # Chart data - only from logged-in user's data
    recent_payments = Payment.objects.filter(status='Paid', tenant__user=user)
    recent_months = recent_payments.annotate(month=TruncMonth('payment_date')) \
        .values('month').annotate(total=Sum('amount_paid')).order_by('-month')[:6]

    monthly_labels = [p['month'].strftime('%b') for p in reversed(recent_months)]
    monthly_data = [p['total'] for p in reversed(recent_months)]

    # ✅ Excel export
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

        writer.writerow([])  # Spacer

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

    # Render page normally
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
        form = TenantForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.user = request.user  # ✅ Link the tenant to the current user
            tenant.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(user=request.user)  # ✅ Pass user here too

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



# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ User Login
from .forms import InactiveUserAuthForm

def login_view(request):
    if request.method == 'POST':
        form = InactiveUserAuthForm(request, data=request.POST)  # Use your custom form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back! You have successfully logged in.")
            return redirect('home')  # Redirect to the dashboard or another view
        else:
            # Process non-field errors and add them to messages
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = InactiveUserAuthForm()  # Initialize the form for GET request

    # Render the login template and pass the form
    return render(request, 'users/login.html', {'form': form})
# ✅ Dashboard







@login_required


def dashboard(request):
    current_user = request.user

    total_tenants = Tenant.objects.filter(user=current_user).count()
    total_employees = Employee.objects.filter(user=current_user).count()
    pending_payments = Payment.objects.filter(user=current_user, status="Pending").count()
    total_paid = Payment.objects.filter(user=current_user).aggregate(total=Sum('amount_paid'))['total'] or 0
    total_payment_list = Payment.objects.filter(user=current_user).count()

    # Latest 2 payments
    recent_payments = Payment.objects.filter(user=current_user).order_by('-payment_date')[:2]

    # Paginated list of payments
    all_payments = Payment.objects.filter(user=current_user).order_by('-payment_date')
    paginator = Paginator(all_payments, 5)  # Show 5 payments per page
    page_number = request.GET.get('page')
    paginated_payments = paginator.get_page(page_number)

    properties = Property.objects.filter(user=current_user)
    total_occupied_units = sum([p.occupied_units for p in properties])
    total_available_units = sum([p.available_units for p in properties])

    context = {
        'total_tenants': total_tenants,
        'total_employees': total_employees,
        'pending_payments': pending_payments,
        'total_paid': total_paid,
        'recent_payments': recent_payments,
        'total_payment_list': total_payment_list,
        'total_occupied_units': total_occupied_units,
        'total_available_units': total_available_units,
        'paginated_payments': paginated_payments,
        'now': now(),
        'user': current_user,
    }

    return render(request, 'users/dashboard.html', context)





@login_required
@login_required
def financial_report(request):
    # Get month from query param or default to current
    month = request.GET.get('month')
    try:
        selected_month = int(month) if month else timezone.now().month
    except ValueError:
        selected_month = timezone.now().month

    year = timezone.now().year
    user = request.user  # Get the logged-in user

    # Payments and Expenses in selected month for the logged-in user
    payments = Payment.objects.filter(payment_date__month=selected_month, payment_date__year=year, user=user)
    expenses = Expense.objects.filter(expense_date__month=selected_month, expense_date__year=year, user=user)

    total_income = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_income - total_expenses

    # Convert Decimal to float for JSON compatibility
    total_income = float(total_income)
    total_expenses = float(total_expenses)
    net_profit = float(net_profit)

    # Monthly chart data for bar chart
    monthly_labels = [calendar.month_name[i] for i in range(1, 13)]
    income_data = [
        float(Payment.objects.filter(payment_date__month=i, payment_date__year=year, user=user).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0)
        for i in range(1, 13)
    ]
    expense_data = [
        float(Expense.objects.filter(expense_date__month=i, expense_date__year=year, user=user).aggregate(Sum('amount'))['amount__sum'] or 0)
        for i in range(1, 13)
    ]

    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]

    context = {
        'selected_month': selected_month,
        'month_choices': month_choices,
        'payments': payments,
        'expenses': expenses,
        'report_summary': {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'chart_labels': json.dumps(monthly_labels),
            'chart_income': json.dumps(income_data),
            'chart_expense': json.dumps(expense_data),
        }
    }

    return render(request, 'tenant/financial_report.html', context)

@login_required
def export_financial_report(request):
    # Get the selected month from GET parameter or use current month
    month = request.GET.get('month')
    if not month:
        month = timezone.now().month

    user = request.user  # Get the logged-in user
    report_summary = generate_financial_report(month=month, user=user)
    
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
        form = ExpenseForm(request.POST,request.FILES)
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



# List all properties for sale
def for_sale_list_view(request):
    query = request.GET.get('q', '')
    property_type = request.GET.get('type', '')

    properties = ForSaleProperty.objects.all()

    if query:
        properties = properties.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )

    if property_type:
        properties = properties.filter(property_type=property_type)

    return render(request, 'users/for_sale_list.html', {
        'properties': properties,
        'query': query,
        'property_type': property_type
    })

# Detail view
def for_sale_detail_view(request, pk):
    property = get_object_or_404(ForSaleProperty, pk=pk)
    return render(request, 'users/for_sale_detail.html', {'property': property})

# Create new property
def for_sale_create_view(request):
    if request.method == 'POST':
        form = ForSalePropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('for_sale_list')
    else:
        form = ForSalePropertyForm()
    return render(request, 'users/for_sale_form.html', {'form': form})






# List commercial properties
def commercial_list_view(request):
    properties = CommercialProperty.objects.all()
    return render(request, 'users/commercial_list.html', {'properties': properties})

# Detail view
def commercial_detail_view(request, pk):
    property = get_object_or_404(CommercialProperty, pk=pk)
    return render(request, 'users/commercial_detail.html', {'property': property})

# Create new commercial property
def commercial_create_view(request):
    if request.method == 'POST':
        form = CommercialPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('commercial_list')
    else:
        form = CommercialPropertyForm()
    return render(request, 'users/commercial_form.html', {'form': form})


from django.core.cache import cache
from django.http import JsonResponse
import requests



def autocomplete_places(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse([], safe=False)

    cached_data = cache.get(query)
    if cached_data is not None:
        return JsonResponse(cached_data, safe=False)

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "countrycodes": "KE",
        "format": "json",
        "limit": 10,
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "YourAppName (contact@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        results = response.json()

        # Trim display_name to only the first part before the comma
        suggestions = []
        for item in results:
            name = item.get("display_name", "")
            if name:
                trimmed = name.split(",")[0].strip().capitalize()
                suggestions.append(trimmed)

        # Remove duplicates
        suggestions = list(dict.fromkeys(suggestions))

        cache.set(query, suggestions, timeout=300)
        return JsonResponse(suggestions, safe=False)

    except requests.RequestException as e:
        print(f"Nominatim API error: {e}")
        return JsonResponse([], safe=False)
