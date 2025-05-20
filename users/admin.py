from django.contrib import admin
from .models import Partner
from .models import  ForSaleProperty, CommercialProperty,VacantRoom
from django.utils.html import format_html



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
    
    readonly_fields = ['video_preview']

    def video_preview(self, obj):
        if obj.video_tour:
            return format_html(f'<video width="320" height="240" controls><source src="{obj.video_tour.url}" type="video/mp4">Your browser does not support the video tag.</video>')
        return "No video"
    video_preview.short_description = "Video Tour Preview"
