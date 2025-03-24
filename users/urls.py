# users/urls.py

from django.urls import path  # Ensure this import is here
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from . import views  # Import views from your app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),  # Redirect root to login
    path('login/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tenant_list/', views.tenant_list, name='tenant_list'),
    path('add_tenant/', views.add_tenant, name='add_tenant'),
    path('edit_tenant/<int:tenant_id>/', views.edit_tenant, name='edit_tenant'),
    path('delete_tenant/<int:tenant_id>/', views.delete_tenant, name='delete_tenant'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


