from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    number_of_units = models.PositiveIntegerField(null=True, blank=True)
    start_date = models.DateField()
    completion_date = models.DateField()

    @property
    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())

    def __str__(self):
        return self.name


class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='units')
    project = models.ForeignKey(Project, related_name='units', on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)  # e.g. 2BHK, Villa
    size_in_sqft = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.unit_number} - {self.project.name}'


class ClientBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    unit = models.ForeignKey(Unit, related_name='bookings', on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name} - {self.unit.unit_number}'

    @property
    def total_payments(self):
        return sum(payment.amount_paid for payment in self.payments.all())

    @property
    def remaining_balance(self):
        return self.unit.price - self.total_payments - self.deposit_amount

    @property
    def is_fully_paid(self):
        return self.remaining_balance <= 0


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Installment', 'Installment'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    booking = models.ForeignKey(ClientBooking, related_name='payments', on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, null=True, blank=True)
    receipt_number = models.CharField(max_length=255, default="DEFAULT123")

    def __str__(self):
        return f'Payment of KES {self.amount_paid} for {self.booking.client_name}'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='general_expenses')
    project = models.ForeignKey(Project, related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Expense for {self.project.name} - KES {self.amount}'


class ConstructionExpense(models.Model):
    EXPENSE_CHOICES = [
        ('materials', 'Materials'),
        ('labor', 'Labor'),
        ('equipment', 'Equipment'),
        ('permits', 'Permits'),
        ('consultants', 'Consultants'),
        ('transport', 'Transport'),
        ('misc', 'Miscellaneous'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='construction_expenses')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='construction_expenses')
    description = models.CharField(max_length=50, choices=EXPENSE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_incurred = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.get_description_display()} - {self.amount}"


class Construction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='constructions')
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='construction')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0)  # 0 to 100
    current_phase = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.progress_percentage}%"