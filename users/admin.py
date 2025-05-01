from django.contrib import admin
from .models import Partner
from .models import  ForSaleProperty, CommercialProperty,VacantRoom

# Register your models here.
admin.site.register(Partner)



@admin.register(ForSaleProperty)
class ForSalePropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'property_type', 'is_available')

@admin.register(CommercialProperty)
class CommercialPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'commercial_type', 'is_available')


@admin.register(VacantRoom)
class VacantRoomAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'title', 'location', 'room_type', 'amount',
        'available_from', 'is_available', 'video_tour', 'created_at'
    )
    list_filter = ('room_type', 'location', 'is_available')
    search_fields = ('title', 'description', 'location')