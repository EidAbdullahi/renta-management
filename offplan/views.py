from django.shortcuts import render, get_object_or_404
from .models import Project, Unit, ClientBooking, Payment
from .forms import ClientBookingForm, PaymentForm
from datetime import date
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from .models import Unit, Project
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required





from django.shortcuts import render, redirect
from .models import Project, Unit
from .forms import ProjectForm, UnitForm

# View to create a new Project
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')  # Redirect to project list after successful creation
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

# View to create a new Unit
@login_required
def create_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save()  # <<< Save and assign to a variable called unit
            return redirect('view_units', project_id=unit.project.id)  # Now this works
    else:
        form = UnitForm()
    return render(request, 'create_unit.html', {'form': form})


# List all Projects
@login_required
def project_list(request):
    projects = Project.objects.all()
    project_data = []

    for project in projects:
        # Get how many units are marked as sold
        sold_units = project.units.filter(is_sold=True).count()

        # Use the number_of_units field from Project
        total_units = project.number_of_units or 0

        # Available units = total units - sold units
        available_units = total_units - sold_units

        project_data.append({
            'project': project,
            'total_units': total_units,
            'sold_units': sold_units,
            'available_units': available_units,
        })

    return render(request, 'project_list.html', {'project_data': project_data})


@login_required
def view_units(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    units = Unit.objects.filter(project=project)
    return render(request, 'unit_list.html', {'project': project, 'units': units})
# Show Unit Details





@login_required
@login_required
def book_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    # Check if the unit is already sold
    if unit.is_sold:
        messages.error(request, "This unit has already been sold.")
        return redirect('view_units', project_id=unit.project.id)

    # Handle the booking form submission
    if request.method == 'POST':
        form = ClientBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.unit = unit  # Link the booking to the unit
            booking.save()

            # Mark the unit as sold
            unit.is_sold = True
            unit.save()

            messages.success(request, f"You have successfully booked Unit {unit.unit_number}!")

            # Redirect to the booking details page
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = ClientBookingForm()

    return render(request, 'booking.html', {'form': form, 'unit': unit})
# Record Payment for a Client Booking
@login_required
def add_payment(request, booking_id):
    booking = get_object_or_404(ClientBooking, id=booking_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'booking': booking})



@login_required
def booked_units(request):
    # Get all available projects for filtering
    projects = Project.objects.all()

    # Initialize the query for filtering
    booked_units = Unit.objects.filter(is_sold=True)

    # Handle filtering by project
    project_filter = request.GET.get('project')
    if project_filter:
        booked_units = booked_units.filter(project__id=project_filter)

    # Handle filtering by unit number
    unit_number_filter = request.GET.get('unit_number')
    if unit_number_filter:
        booked_units = booked_units.filter(unit_number__icontains=unit_number_filter)

    # Sorting by unit number
    sort_by = request.GET.get('sort_by', 'unit_number')  # Default sort by unit number
    booked_units = booked_units.order_by(sort_by)

    # Implementing pagination
    page = request.GET.get('page', 1)  # Default to page 1
    paginator = Paginator(booked_units, 10)  # Show 10 units per page
    page_obj = paginator.get_page(page)

    # For each unit, calculate how many bookings have a deposit_amount greater than 0
    for unit in page_obj:
        unit.bookings_with_deposit_count = unit.bookings.filter(deposit_amount__gt=0).count()

    return render(request, 'booked_units.html', {
        'booked_units': page_obj,
        'projects': projects,
        'project_filter': project_filter,
        'unit_number_filter': unit_number_filter,
    })

def booking_details(request, booking_id):
    # Fetch the booking
    booking = get_object_or_404(ClientBooking, id=booking_id)

    # Fetch all payments related to this booking
    payments = booking.payments.all()
    
    # Calculate total paid amount
    total_paid = sum(payment.amount_paid for payment in payments)
    
    # Calculate the remaining balance
    remaining_balance = booking.unit.price - total_paid - booking.deposit_amount

    # If the booking is not fully paid, provide an option to make more payments
    is_fully_paid = booking.is_fully_paid

    # Fetch the bookings for the unit with a deposit_amount greater than 0
    bookings_with_deposit = booking.unit.bookings.filter(deposit_amount__gt=0)

    # Count bookings with deposit
    bookings_with_deposit_count = bookings_with_deposit.count()

    context = {
        'booking': booking,
        'payments': payments,
        'total_paid': total_paid,
        'remaining_balance': remaining_balance,
        'is_fully_paid': is_fully_paid,
        'bookings_with_deposit_count': bookings_with_deposit_count,  # Add this to context
    }

    return render(request, 'booking_details.html', context)