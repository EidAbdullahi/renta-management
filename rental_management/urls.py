from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # ✅ Include users app URLs
    path('freelancers/', include('freelancers.urls')),
    
]
