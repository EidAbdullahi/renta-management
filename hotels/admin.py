from django.contrib import admin
from .models import Hotel, RoomType, Reservation, Amenity, HotelImage

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'star_rating')
    search_fields = ('name', 'location')
    list_filter = ('star_rating',)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'capacity', 'price_per_night', 'quantity')
    search_fields = ('name', 'hotel__name')
    list_filter = ('hotel',)
    filter_horizontal = ('amenities',)  # For ManyToManyField


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room_type', 'check_in', 'check_out', 'created_at')
    list_filter = ('check_in', 'check_out', 'room_type__hotel')
    search_fields = ('guest_name', 'guest_email', 'room_type__name')
    raw_id_fields = ('user',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'is_main')
    list_filter = ('is_main',)
