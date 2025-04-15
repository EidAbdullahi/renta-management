from django.db import models
# users/models.py
from django.db import models
from django.utils import timezone
from django.db.models import Sum

# class MaintenanceRequest(models.Model):
#     tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
#     property = models.ForeignKey('Property', on_delete=models.CASCADE)
#     description = models.TextField()
#     date_requested = models.DateTimeField(default=timezone.now)
#     date_resolved = models.DateTimeField(null=True, blank=True)
#     status_choices = [
#         ('OPEN', 'Open'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('RESOLVED', 'Resolved'),
#     ]
#     status = models.CharField(max_length=15, choices=status_choices, default='OPEN')
#     assigned_to = models.CharField(max_length=255, null=True, blank=True)
#     notes = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Request from {self.tenant.name} - {self.status}"
    
class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    number_of_units = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def occupied_units(self):

      return self.tenants.count()  # No filter

    @property
    def available_units(self):
      if self.number_of_units is not None:
        return self.number_of_units - self.occupied_units
      return 0



class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=6)
    emergency_contact = models.CharField(max_length=15)
    upload_id = models.FileField(upload_to='employee_ids/')
    face_image = models.ImageField(upload_to='employee_faces/', null=True, blank=True)

    def __str__(self):
        return self.full_name



class Tenant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    property = models.ForeignKey(Property, related_name='tenants', on_delete=models.CASCADE,blank=True,null=True)
    move_in_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    id_document = models.FileField(upload_to='tenant_documents/', blank=True, null=True)
    unit_number = models.CharField(max_length=50, blank=True, null=True)


    def calculate_monthly_balance(self):
        current_month = timezone.now().month
        # Get total payments made in the current month
        total_paid = Payment.objects.filter(
            tenant=self,
            payment_date__month=current_month
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        balance = self.rent_amount - total_paid
        return balance

    def overdue_months(self):
        overdue_payments = []
        for payment in Payment.objects.filter(tenant=self):
            if payment.status == 'Pending' and payment.payment_date.month < timezone.now().month:
                overdue_payments.append(payment.payment_date.month)
        return overdue_payments

    def __str__(self):
        return self.name


    
from django.db import models
from django.utils import timezone

class Payment(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)

    PAYMENT_METHODS = [
        ('M-Pesa', 'M-Pesa'),
        ('Bank', 'Bank Transfer'),
        ('Cash', 'Cash'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def update_payment_status(self):
        """Update payment status based on amount and current month."""
        if self.payment_date.month == timezone.now().month:
            if self.amount_paid < self.tenant.rent_amount:
                self.status = 'Overdue'
            else:
                self.status = 'Paid'

    def save(self, *args, **kwargs):
        self.update_payment_status()  # Always update before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant.name} - {self.amount_paid} ({self.status})"


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('Maintenance', 'Maintenance'),
        ('Salaries', 'Salaries'),
        ('Utilities', 'Utilities'),
        ('Repairs', 'Repairs'),
        ('Other', 'Other'),
    ]

    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.expense_type} - KES {self.amount} on {self.expense_date}"

# class Property(models.Model):
#     name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_rented = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name
