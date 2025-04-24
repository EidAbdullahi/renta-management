from django.contrib import admin
from .models import Partner
from .models import  ForSaleProperty, CommercialProperty

# Register your models here.
admin.site.register(Partner)



@admin.register(ForSaleProperty)
class ForSalePropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'property_type', 'is_available')

@admin.register(CommercialProperty)
class CommercialPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'commercial_type', 'is_available')