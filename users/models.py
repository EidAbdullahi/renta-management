from django.db import models
# users/models.py
from django.db import models
from django.utils import timezone

class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    description = models.TextField()
    date_requested = models.DateTimeField(default=timezone.now)
    date_resolved = models.DateTimeField(null=True, blank=True)
    status_choices = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='OPEN')
    assigned_to = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Request from {self.tenant.name} - {self.status}"


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
    property_address = models.CharField(max_length=255)
    move_in_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    id_document = models.FileField(upload_to='tenant_documents/', blank=True, null=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # ✅ Fixed here
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)  # Add receipt upload field

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

    def __str__(self):
        return f"{self.tenant.name} - {self.amount_paid} ({self.status})"
    

class Property(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return self.name
