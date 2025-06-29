from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, RoomType, Reservation
from .forms import SearchForm, BookingForm
from .utils import get_available_room_types
from datetime import datetime


def hotel_search(request):
    form = SearchForm(request.GET or None)
    hotels = []
    check_in = check_out = None
    error_message = None

    if form.is_valid():
        destination = form.cleaned_data.get('destination')
        name = form.cleaned_data.get('name')
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        total_guests = (
            int(form.cleaned_data['adults']) +
            int(form.cleaned_data['children']) +
            int(form.cleaned_data['infants'])
        )

        if check_in > check_out:
            error_message = "Check-in date cannot be after check-out date."
        else:
            hotels_query = Hotel.objects.all()
            if destination:
                hotels_query = hotels_query.filter(location__icontains=destination)
            if name:
                hotels_query = hotels_query.filter(name__icontains=name)

            for hotel in hotels_query:
                available_types = get_available_room_types(hotel, check_in, check_out, total_guests)
                if available_types:
                    hotels.append(hotel)

    return render(request, 'search_hotel.html', {
        'form': form,
        'hotels': hotels,
        'check_in': check_in,
        'check_out': check_out,
        'error_message': error_message,
    })


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')

    # Guest counts
    adults = request.GET.get('adults', '1')
    children = request.GET.get('children', '0')
    infants = request.GET.get('infants', '0')

    try:
        total_guests = int(adults) + int(children) + int(infants)
    except ValueError:
        total_guests = 1
        error_message = "Invalid guest numbers. Defaulting to 1 guest."
    else:
        error_message = None

    def try_parse_date(date_str):
        for fmt in ('%Y-%m-%d', '%B %d, %Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except (ValueError, TypeError):
                continue
        return None

    check_in = try_parse_date(check_in_str)
    check_out = try_parse_date(check_out_str)

    available_room_types = []
    if check_in and check_out:
        available_room_types = get_available_room_types(hotel, check_in, check_out, total_guests)
    else:
        error_message = error_message or "Please provide valid check-in and check-out dates."

    return render(request, 'hotel_detail.html', {
        'hotel': hotel,
        'available_room_types': available_room_types,
        'check_in': check_in_str,
        'check_out': check_out_str,
        'error_message': error_message,
        'adults': adults,
        'children': children,
        'infants': infants,
    })


def book_room_type(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    hotel = room_type.hotel

    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')

    def try_parse_date(date_str):
        for fmt in ('%Y-%m-%d', '%B %d, %Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except (ValueError, TypeError):
                continue
        return None

    check_in = try_parse_date(check_in_str)
    check_out = try_parse_date(check_out_str)

    if request.method == 'POST':
        form = BookingForm(request.POST, room_type=room_type)
        if form.is_valid():
            reservation = form.save()
            return redirect('reservation_receipt', reservation_id=reservation.id)

    else:
        form = BookingForm(
            room_type=room_type,
            initial={
                'check_in': check_in,
                'check_out': check_out,
            }
        )

    return render(request, 'book_room.html', {
        'form': form,
        'room_type': room_type,
        'hotel': hotel,
        'check_in': check_in,
        'check_out': check_out,
    })


def reservation_success(request):
    return render(request, 'hotels/reservation_success.html')


from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint  

def reservation_receipt(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    room_type = reservation.room_type
    hotel = room_type.hotel

    nights = (reservation.check_out - reservation.check_in).days
    total_price = nights * room_type.price_per_night

    if request.GET.get('format') == 'pdf':
        html = render_to_string('receipt.html', {
            'reservation': reservation,
            'hotel': hotel,
            'nights': nights,
            'total_price': total_price,
        })
        pdf_file = weasyprint.HTML(string=html).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{reservation.id}.pdf"'
        return response

    return render(request, 'receipt.html', {
        'reservation': reservation,
        'hotel': hotel,
        'nights': nights,
        'total_price': total_price,
    })



# dashboard/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from hotels.models import Hotel, RoomType, Reservation
from datetime import date
from django.utils.timezone import now
from django.core.paginator import Paginator
@staff_member_required
def dashboard_view(request):
    today = now().date()

    total_hotels = Hotel.objects.count()
    total_reservations = Reservation.objects.count()

    all_active = Reservation.objects.filter(check_out__gte=today).order_by('check_in')
    paginator = Paginator(all_active, 10)  # Show 10 reservations per page
    page_number = request.GET.get('page')
    active_reservations = paginator.get_page(page_number)

    successful_reservations = Reservation.objects.filter(status='successful')
    upcoming_reservations = all_active.filter(check_in__gt=today)

    context = {
        'total_hotels': total_hotels,
        'total_reservations': total_reservations,
        'active_reservations': active_reservations,
        'upcoming_reservations': upcoming_reservations,
        'successful_count': successful_reservations.count(),
    }
    return render(request, 'hotel_dashboard.html', context)

@staff_member_required
def reservation_list(request):
    reservations = Reservation.objects.select_related('room_type', 'room_type__hotel').order_by('-created_at')
    return render(request, 'dashboard/reservations.html', {'reservations': reservations})


from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@require_POST
def mark_successful(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.status = 'successful'
    reservation.save()
    return redirect('hotel_dashboard')

@require_POST
def mark_unsuccessful(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.status = 'unsuccessful'
    reservation.delete()
    return redirect('hotel_dashboard')
