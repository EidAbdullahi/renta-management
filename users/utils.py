from datetime import date
from .models import Payment, Tenant
from django.db.models import Q

def get_unpaid_tenants_for_month(year, month):
    paid_tenants = Payment.objects.filter(
        payment_date__year=year,
        payment_date__month=month,
        status='Paid'
    ).values_list('tenant_id', flat=True)

    unpaid_tenants = Tenant.objects.exclude(id__in=paid_tenants)
    return unpaid_tenants

def get_paid_tenants_for_month(year, month):
    return Payment.objects.filter(
        payment_date__year=year,
        payment_date__month=month,
        status='Paid'
    ).select_related('tenant')
