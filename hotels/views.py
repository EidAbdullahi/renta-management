from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, Reservation
from .forms import SearchForm, BookingForm
from .utils import get_available_rooms
from datetime import datetime
from django.http import Http404

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
        adults = int(form.cleaned_data['adults'])
        children = int(form.cleaned_data['children'])
        infants = int(form.cleaned_data['infants'])

        total_guests = adults + children + infants

        if check_in > check_out:
            error_message = "Check-in date cannot be after check-out date."
        else:
            hotel_query = Hotel.objects.all()
            if destination:
                hotel_query = hotel_query.filter(location__icontains=destination)
            if name:
                hotel_query = hotel_query.filter(name__icontains=name)

            for hotel in hotel_query:
                rooms = get_available_rooms(hotel, check_in, check_out, total_guests)
                if rooms:
                    hotels.append(hotel)

    return render(request, 'search_hotel.html', {
        'form': form,
        'hotels': hotels,
        'check_in': check_in,
        'check_out': check_out,
        'error_message': error_message,
    })

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Hotel
from .utils import get_available_rooms

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')
    available_rooms = []
    error_message = None

    # Parse guest counts
    adults = request.GET.get('adults', '1')
    children = request.GET.get('children', '0')
    infants = request.GET.get('infants', '0')

    try:
        total_guests = int(adults) + int(children) + int(infants)
    except ValueError:
        total_guests = 1
        error_message = "Invalid guest numbers. Defaulting to 1 guest."

    print(f"hotel_detail called for hotel id: {hotel_id}")
    print(f"Received check_in: {check_in_str}, check_out: {check_out_str}, guests: {total_guests}")

    def try_parse_date(date_str):
        """Try parsing with multiple formats."""
        for fmt in ('%Y-%m-%d', '%B %d, %Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except (ValueError, TypeError):
                continue
        return None

    if check_in_str and check_out_str:
        check_in = try_parse_date(check_in_str)
        check_out = try_parse_date(check_out_str)

        if not check_in or not check_out:
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            print(f"Date parsing error: {error_message}")
        else:
            print(f"Parsed dates - check_in: {check_in}, check_out: {check_out}")
            available_rooms = get_available_rooms(hotel, check_in, check_out, total_guests)
            print(f"Found {len(available_rooms)} available rooms:")
            for room in available_rooms:
                print(f" - Room {room.room_number} of type {room.room_type.name}")
    else:
        print("No check-in or check-out dates provided.")

    context = {
        'hotel': hotel,
        'available_rooms': available_rooms,
        'check_in': check_in_str,
        'check_out': check_out_str,
        'error_message': error_message,
        'adults': adults,
        'children': children,
        'infants': infants,
    }
    return render(request, 'hotel_detail.html', context)




def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    hotel = room.room_type.hotel

    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')
    check_in = check_out = None

    # Parse strings like "June 26, 2025"
    try:
        if check_in_str:
            check_in = datetime.strptime(check_in_str, '%B %d, %Y').date()
        if check_out_str:
            check_out = datetime.strptime(check_out_str, '%B %d, %Y').date()
    except ValueError:
        pass  # You can log this if needed

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            form.save()

            # Clear form after successful submission
            form = BookingForm(room=room)

            return render(request, 'book_room.html', {
                'form': form,
                'room': room,
                'hotel': hotel,
                'check_in': check_in,
                'check_out': check_out,
                'success': True  # Used to trigger the success message in the template
            })
    else:
        form = BookingForm(
            room=room,
            initial={
                'check_in': check_in,
                'check_out': check_out,
            }
        )

    return render(request, 'book_room.html', {
        'form': form,
        'room': room,
        'hotel': hotel,
        'check_in': check_in,
        'check_out': check_out,
    })

def reservation_success(request):
    return render(request, 'hotels/reservation_success.html')
