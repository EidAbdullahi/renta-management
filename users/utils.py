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



# utils.py
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_invoice_pdf(payment):
    template = get_template('tenant/payment_invoice_pdf.html')
    html = template.render({'payment': payment})
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return None
    return result


# utils.py (continued or separate file)
from django.core.mail import EmailMessage

def send_invoice_email(payment):
    pdf = generate_invoice_pdf(payment)
    if not pdf:
        return

    email = EmailMessage(
        subject=f"Invoice for Payment #{payment.id}",
        body="Attached is your payment invoice. Thank you!",
        from_email="your_gmail@gmail.com",
        to=[payment.tenant.email]
    )
    email.attach(f'invoice_{payment.id}.pdf', pdf.getvalue(), 'application/pdf')
    email.send()
