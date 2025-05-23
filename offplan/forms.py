from django import forms
from .models import ClientBooking, Payment
from .models import Unit
from .models import Project
from datetime import date
from .models import ConstructionExpense


from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'location', 'number_of_units', 'start_date', 'completion_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter project name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter location'
            }),
            'number_of_units': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Number of units'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'completion_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
        }


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Project name cannot be empty.")
        return name

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['project', 'unit_number', 'unit_type', 'size_in_sqft', 'price']

    def clean_unit_number(self):
        unit_number = self.cleaned_data.get('unit_number')
        if not unit_number:
            raise forms.ValidationError("Unit number cannot be empty.")
        return unit_number

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user is not None:
            self.fields['project'].queryset = Project.objects.filter(user=self.user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class ClientBookingForm(forms.ModelForm):
    class Meta:
        model = ClientBooking
        fields = ['client_name', 'client_email', 'client_phone', 'deposit_amount']

    def clean_deposit_amount(self):
        deposit = self.cleaned_data.get('deposit_amount')
        if deposit <= 0:
            raise forms.ValidationError("Deposit amount must be positive.")
        return deposit


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid', 'payment_type', 'receipt_number']
        
    def clean_amount_paid(self):
        amount = self.cleaned_data.get('amount_paid')
        if amount <= 0:
            raise forms.ValidationError("Amount paid must be positive.")
        return amount




class ConstructionExpenseForm(forms.ModelForm):
    class Meta:
        model = ConstructionExpense
        fields = ['project', 'description', 'amount', 'date_incurred']
        widgets = {
            'date_incurred': forms.DateInput(attrs={'type': 'date'}),
        }

        project = forms.ModelChoiceField(queryset=Project.objects.all(), label="Select Project")
