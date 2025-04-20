from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class VacantRoom(models.Model):
    ROOM_TYPE_CHOICES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Self-Contained', 'Self-Contained'),
        ('Bedsitter', 'Bedsitter'),
        ('1 Bedroom', '1 Bedroom'),
        ('2 Bedroom', '2 Bedroom'),
        ('3 Bedroom', '3 Bedroom'),
        ('4 Bedroom', '4 Bedroom'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacant_rooms')
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    picture1 = models.ImageField(upload_to='vacancy_images/', null=True, blank=True)
    picture2 = models.ImageField(upload_to='vacancy_images/', null=True, blank=True)
    picture3 = models.ImageField(upload_to='vacancy_images/', null=True, blank=True)
    available_from = models.DateField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.location}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('vacancy_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense')
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



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

    def __str__(self):
        return f'{self.user.username} Profile'
    

# class Property(models.Model):
#     name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_rented = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name
