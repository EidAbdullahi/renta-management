def get_available_rooms(hotel, check_in, check_out, total_guests):
    print(f"Checking availability for hotel: {hotel.name} between {check_in} and {check_out} for {total_guests} guests")

    available_rooms = []
    room_types = hotel.room_types.prefetch_related('rooms').all()

    for room_type in room_types:
        print(f"Room Type: {room_type.name} (Capacity: {room_type.capacity})")
        for room in room_type.rooms.all():
            conflicts = room.reservations.filter(
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            print(f"Room {room.room_number} has {conflicts.count()} conflicting reservations")
            if not conflicts.exists():
                if room_type.capacity >= total_guests:
                    print(f"Room {room.room_number} is available and fits {total_guests} guests")
                    available_rooms.append(room)
                else:
                    print(f"Room {room.room_number} is available but too small (capacity: {room_type.capacity})")

    print(f"Total available rooms found: {len(available_rooms)}")
    return available_rooms
