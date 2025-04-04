from django import forms
from .models import Tenant
from django import forms
from .models import Payment, Tenant
from django import forms
from .models import Employee

# users/forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'position', 'salary', 'gender', 'emergency_contact', 'upload_id']
        widgets = {
            'position': forms.Select(choices=[('Manager', 'Manager'), ('Guard', 'Guard'), ('Cleaner', 'Cleaner')]),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
        }


class PaymentForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        empty_label="Select Tenant",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Payment
        fields = ['tenant', 'payment_date', 'amount_paid', 'payment_method', 'status', 'receipt']  # Add receipt
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control'})  # Add this
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'  # Or list fields explicitly

    # Ensure correct file input handling
    # photo = forms.ImageField(required=False)
    id_document = forms.FileField(required=False)
