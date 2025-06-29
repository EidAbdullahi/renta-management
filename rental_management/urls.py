from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secret-admin-4444/', admin.site.urls),
    path('', include('users.urls')),
    path('freelancers/', include('freelancers.urls')),
    path('offplan/', include('offplan.urls')),
    path('hotel/', include('hotels.urls')),
]

# ✅ Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
