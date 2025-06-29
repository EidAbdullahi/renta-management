def get_available_room_types(hotel, check_in, check_out, total_guests):
    print(f"Checking availability for hotel: {hotel.name} between {check_in} and {check_out} for {total_guests} guests")

    room_types_data = []

    for room_type in hotel.room_types.all():
        print(f"Checking Room Type: {room_type.name} (Capacity: {room_type.capacity}, Quantity: {room_type.quantity})")

        if room_type.capacity < total_guests:
            print(f"  Skipped: Capacity {room_type.capacity} is less than guest count {total_guests}")
            continue

        # Count only overlapping reservations
        overlapping = room_type.reservations.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).count()

        available_count = room_type.quantity - overlapping

        # ✅ Forcefully allow full quantity if no overlap
        if overlapping == 0:
            available_count = room_type.quantity

        print(f"  Overlapping reservations: {overlapping}")
        print(f"  Available count: {available_count}")

        room_type.available_count = available_count
        room_types_data.append(room_type)

    print(f"Total room types returned: {len(room_types_data)}")
    return room_types_data
