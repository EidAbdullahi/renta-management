from django.contrib import admin
from .models import Hotel, RoomType, Room, Reservation
from .models import Amenity
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'star_rating')
    search_fields = ('name', 'location')
    list_filter = ('star_rating',)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'capacity', 'price_per_night')
    search_fields = ('name', 'hotel__name')
    list_filter = ('hotel',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'get_hotel', 'is_available')
    list_filter = ('room_type__hotel', 'is_available')
    search_fields = ('room_number',)

    def get_hotel(self, obj):
        return obj.room_type.hotel.name
    get_hotel.short_description = 'Hotel'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in', 'check_out', 'created_at')
    list_filter = ('check_in', 'check_out')
    search_fields = ('guest_name', 'guest_email', 'room__room_number')
    raw_id_fields = ('room', 'user')


from django.contrib import admin
from .models import Amenity

admin.site.register(Amenity)
