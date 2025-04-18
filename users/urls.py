from django.urls import path  
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import payment_list, tenant_payments
from .views import (
    dashboard, tenant_list, add_tenant, edit_tenant, delete_tenant, 
    add_payment, payment_list, update_rent_status, edit_payment
)

urlpatterns = [
    path('payments/', payment_list, name='payment_list'),  # View all payments
    path('payments/tenant/<int:tenant_id>/', tenant_payments, name='tenant_payments'),  # View payments for a specific tenant
    # Redirect root to login
    path('', lambda request: redirect('login'), name='home'),
    path('payment-summary/', views.payment_summary, name='payment_summary'),
    path('export-csv/', views.export_payments_csv, name='export_payments_csv'),

    # Authentication
    path('login/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Tenant Management

    path('tenant_list/', tenant_list, name='tenant_list'),
    path('add_tenant/', add_tenant, name='add_tenant'),
    path('edit_tenant/<int:tenant_id>/', edit_tenant, name='edit_tenant'),
    path('delete_tenant/<int:tenant_id>/', delete_tenant, name='delete_tenant'),

    # Payment Management
    path('payments/', payment_list, name='payment_list'),
    # path('add-payment/', add_payment, name='add_payment'),  # Add Payment (without tenant)
    path('add-payment/<int:tenant_id>/', add_payment, name='add_payment_tenant'),  # Add Payment for specific tenant
    path('payments/', payment_list, name='payment_list'),  # View all payments
    # Rent Status Update
    path('update-rent-status/<int:tenant_id>/', update_rent_status, name='update_rent_status'),
    path('add-payment/<int:tenant_id>/', add_payment, name='add_payment'),
    
    path('register_employee/', views.register_employee, name='register_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('edit_employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),




    # URL for the financial report summary page
    path('financial-report/', views.financial_report, name='financial_report'),
    
    # URL for exporting the financial report to CSV
    path('export-financial-report/', views.export_financial_report, name='export_financial_report'),
    

    path('add-expense/', views.add_expense, name='add_expense'),
    path('expense-list/', views.expense_list, name='expense_list'),


    path('properties/', views.property_list, name='property_list'),
    path('properties/add/', views.add_property, name='add_property'),
    
    path('payments/edit/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('payments/delete/<int:payment_id>/', views.delete_payment, name='delete_payment'),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
