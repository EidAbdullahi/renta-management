from django.db import models

class Project(models.Model):
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
    project = models.ForeignKey(Project, related_name='units', on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)  # e.g. 2BHK, Villa, etc.
    size_in_sqft = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.unit_number} - {self.project.name}'


class ClientBooking(models.Model):
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
    booking = models.ForeignKey(ClientBooking, related_name='payments', on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, choices=[('Deposit', 'Deposit'), ('Installment', 'Installment')],null=True ,blank=True)
    receipt_number = models.CharField(max_length=255, default="DEFAULT123")  # Set default here

    def __str__(self):
        return f'Payment of KES {self.amount_paid} for {self.booking.client_name}'


class Expense(models.Model):
    project = models.ForeignKey(Project, related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Expense for {self.project.name} - KES {self.amount}'
