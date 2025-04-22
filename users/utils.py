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

from django.utils.timezone import now
from django.db.models import Sum
from .models import Payment, Expense

from django.db.models import Sum
from django.utils.timezone import now

def generate_financial_report(request, month=None):
    if month is None:
        month = now().month
    year = now().year
    
    # Get the currently logged-in user
    user = request.user
    
    # Filter Payments by the current user, month, and year
    total_income = Payment.objects.filter(
        tenant__user=user,  # Assuming 'tenant' is linked to 'user'
        payment_date__month=month,
        payment_date__year=year
    ).aggregate(total=Sum('amount_paid'))['total'] or 0

    # Filter Expenses by the current user, month, and year
    total_expenses = Expense.objects.filter(
        user=user,  # Assuming Expense is linked to 'user'
        expense_date__month=month,
        expense_date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate net profit
    net_profit = total_income - total_expenses

    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit
    }
