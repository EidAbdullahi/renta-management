from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Sum, Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    ClientBookingForm,
    PaymentForm,
    ProjectForm,
    UnitForm,
    ConstructionExpenseForm,
)
from .models import (
    Project,
    Unit,
    ClientBooking,
    Payment,
    Construction,
    ConstructionExpense,
)

# ====================== PROJECT VIEWS ======================

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # <-- assign logged-in user here
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@login_required
def project_list(request):
    # Filter projects for the current user only
    projects = Project.objects.filter(user=request.user)
    project_data = []

    for project in projects:
        sold_units = project.units.filter(is_sold=True).count()
        total_units = project.number_of_units or 0
        available_units = total_units - sold_units

        project_data.append({
            'project': project,
            'total_units': total_units,
            'sold_units': sold_units,
            'available_units': available_units,
        })

    return render(request, 'project_list.html', {'project_data': project_data})



# ====================== UNIT VIEWS ======================

@login_required
@login_required
def create_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST, user=request.user)  # pass user here too!
        if form.is_valid():
            form.save()
            messages.success(request, "Unit created successfully!")
            return redirect('unit_list')  # or appropriate URL
    else:
        form = UnitForm(user=request.user)  # pass user on GET too!

    return render(request, 'create_unit.html', {'form': form})



@login_required
def view_units(request, project_id):
    # Ensure the project belongs to the current user
    project = get_object_or_404(Project, id=project_id, user=request.user)

    # Filter units related to this project
    units = Unit.objects.filter(project=project)

    return render(request, 'unit_list.html', {
        'project': project,
        'units': units
    })

@login_required
def booked_units(request):
    # Only show projects owned by the logged-in user
    projects = Project.objects.filter(user=request.user)
    # Filter booked units that belong to those projects
    booked_units = Unit.objects.filter(is_sold=True, project__user=request.user)

    project_filter = request.GET.get('project')
    if project_filter:
        booked_units = booked_units.filter(project__id=project_filter)

    unit_number_filter = request.GET.get('unit_number')
    if unit_number_filter:
        booked_units = booked_units.filter(unit_number__icontains=unit_number_filter)

    sort_by = request.GET.get('sort_by', 'unit_number')
    booked_units = booked_units.order_by(sort_by)

    paginator = Paginator(booked_units, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    for unit in page_obj:
        unit.bookings_with_deposit_count = unit.bookings.filter(deposit_amount__gt=0).count()

    return render(request, 'booked_units.html', {
        'booked_units': page_obj,
        'projects': projects,
        'project_filter': project_filter,
        'unit_number_filter': unit_number_filter,
    })


# ====================== BOOKING & PAYMENT ======================

@login_required
@login_required
def book_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    if unit.is_sold:
        messages.error(request, "This unit has already been sold.")
        return redirect('view_units', project_id=unit.project.id)

    if request.method == 'POST':
        form = ClientBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.unit = unit
            booking.user = request.user  
            booking.save()

            unit.is_sold = True
            unit.save()

            messages.success(request, f"You have successfully booked Unit {unit.unit_number}!")
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = ClientBookingForm()

    return render(request, 'booking.html', {'form': form, 'unit': unit})


@login_required
def booking_details(request, booking_id):
    booking = get_object_or_404(ClientBooking, id=booking_id)

    # Check if the logged-in user owns the project of this unit
    if booking.unit.project.user != request.user:
        return HttpResponseForbidden("You do not have permission to view this booking.")

    payments = booking.payments.all()
    total_paid = sum(payment.amount_paid for payment in payments)
    remaining_balance = booking.unit.price - total_paid - booking.deposit_amount
    is_fully_paid = booking.is_fully_paid

    bookings_with_deposit_count = booking.unit.bookings.filter(deposit_amount__gt=0).count()

    return render(request, 'booking_details.html', {
        'booking': booking,
        'payments': payments,
        'total_paid': total_paid,
        'remaining_balance': remaining_balance,
        'is_fully_paid': is_fully_paid,
        'bookings_with_deposit_count': bookings_with_deposit_count,
    })

@login_required
def add_payment(request, booking_id):
    booking = get_object_or_404(ClientBooking, id=booking_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.user = request.user  # ✅ Important line
            payment.save()

            messages.success(request, "Payment added successfully.")
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'add_payment.html', {'form': form, 'booking': booking})



# ====================== DASHBOARD ======================

@login_required
def offplan_dashboard(request):
    user = request.user

    # Filter projects and related objects by user
    projects = Project.objects.filter(user=user)
    all_units = Unit.objects.filter(project__user=user)
    bookings = ClientBooking.objects.filter(unit__project__user=user)
    constructions = Construction.objects.filter(project__user=user)
    expenses = ConstructionExpense.objects.filter(project__user=user)

    context = {
        'total_projects': projects.count(),
        'total_units': all_units.count(),
        'units_sold': all_units.filter(is_sold=True).count(),
        'available_units': all_units.filter(is_sold=False).count(),
        'booked_units': bookings.values('unit').distinct().count(),
        'average_progress': round(constructions.aggregate(avg=Avg('progress_percentage'))['avg'] or 0),
        'total_construction_expenses': expenses.aggregate(total=Sum('amount'))['total'] or 0,
        'now': datetime.now(),
        'user': user,
    }

    return render(request, 'offplan_dashboard.html', context)

# ====================== CONSTRUCTION EXPENSE ======================


@login_required
def add_construction_expense(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ConstructionExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.user = request.user  # <-- assign user here
            expense.save()
            messages.success(request, "Construction expense added successfully.")
            return redirect('project_expenses', project_id=project.id)
    else:
        form = ConstructionExpenseForm(initial={'project': project})

    return render(request, 'add_expense.html', {'form': form, 'project': project})


@login_required
def project_expenses(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    expenses = project.construction_expenses.all()
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'expense_list.html', {
        'project': project,
        'expenses': expenses,
        'total_expenses': total_expenses,
    })
