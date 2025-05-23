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
# users/utils.py

from django.utils import timezone
from django.db.models import Sum
from .models import Payment, Expense

from django.db.models import Sum
from django.utils.timezone import now
def generate_financial_report(month, user):
    year = timezone.now().year

    payments = Payment.objects.filter(payment_date__month=month, payment_date__year=year, user=user)
    expenses = Expense.objects.filter(expense_date__month=month, expense_date__year=year, user=user)

    total_income = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_income - total_expenses

    return {
        'month': month,
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'net_profit': float(net_profit),
    }

