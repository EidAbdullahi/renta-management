from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User
# models.py
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'Rent Property'),
        ('commercial', 'Commercial Property'),
        ('marketplace', 'Marketplace Item'),
        ('forsale', 'Property For Sale'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    item_title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item_title} - {self.amount}"


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Furniture', 'Furniture'),
        ('Electronics', 'Electronics'),
        ('Kitchen', 'Kitchen'),
        ('Clothing', 'Clothing'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reactions')
    session_id = models.CharField(max_length=100)  # Anonymous or logged-in user session
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    reacted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('item', 'session_id', 'reaction_type')

from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.utils.timesince import timesince
from django.utils.timezone import now

class VacantRoom(models.Model):
    ROOM_TYPE_CHOICES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Self-Contained', 'Self-Contained'),
        ('Bedsitter', 'Bedsitter'),
        ('Airbnb', 'Airbnb'),
        ('Duplex', 'Duplex'), 
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

    picture1 = CloudinaryField('image', null=True, blank=True)
    picture2 = CloudinaryField('image', null=True, blank=True)
    picture3 = CloudinaryField('image', null=True, blank=True)
    video_tour = CloudinaryField('video', null=True, blank=True)

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

    def get_images(self):
        return [self.picture1, self.picture2, self.picture3]

    def posted_ago(self):
        return timesince(self.created_at, now()) + " ago"

    def __str__(self):
        return f"{self.title} - {self.room_type} - {self.location}"

    

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=6)
    emergency_contact = models.CharField(max_length=15)
    upload_id = CloudinaryField('file')  # changed from FileField
    face_image = CloudinaryField('image', null=True, blank=True)
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
    id_document = CloudinaryField('file', blank=True, null=True)
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
    receipt = CloudinaryField('file', blank=True, null=True)

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
    receipt = CloudinaryField('file', blank=True, null=True)
    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.expense_type} - KES {self.amount} on {self.expense_date}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    image = CloudinaryField('image', default='profile_pics/default.jpg')

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

    def __str__(self):
        return f'{self.user.username} Profile'
    



class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = CloudinaryField('image')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name





class ForSaleProperty(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Land', 'Land'),
        ('Townhouse', 'Townhouse'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sale_properties')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPE_CHOICES)
    lot_size = models.CharField(max_length=50, null=True, blank=True)
    built_year = models.IntegerField(null=True, blank=True)
    picture1 = CloudinaryField('image', null=True, blank=True)
    picture2 = CloudinaryField('image', null=True, blank=True)
    picture3 = CloudinaryField('image', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('for_sale_detail', kwargs={'pk': self.pk})

class CommercialProperty(models.Model):
    COMMERCIAL_TYPE_CHOICES = (
        ('Office', 'Office'),
        ('Retail', 'Retail'),
        ('Warehouse', 'Warehouse'),
        ('Industrial', 'Industrial'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commercial_properties')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=100)
    commercial_type = models.CharField(max_length=30, choices=COMMERCIAL_TYPE_CHOICES)
    floor_space = models.DecimalField(max_digits=10, decimal_places=2, help_text="In square meters")
    parking_spaces = models.IntegerField(null=True, blank=True)
    picture1 = CloudinaryField('image', null=True, blank=True)
    picture2 = CloudinaryField('image', null=True, blank=True)
    picture3 = CloudinaryField('image', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

from django.db import models

class FreelancerContact(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    help_text = models.TextField(verbose_name="How can we help?")
    date = models.DateField()
    address = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.contact}"
