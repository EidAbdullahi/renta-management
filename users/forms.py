from django import forms
from .models import Tenant
from django import forms
from .models import Payment, Tenant
from django import forms
from .models import Employee
from .models import Expense
from django import forms
from .models import Expense
# users/forms.py
from django import forms
from .models import Employee

from django import forms
from .models import Employee
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'number_of_units']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'full_name',
            'email',
            'phone',
            'position',
            'salary',
            'gender',
            'emergency_contact',
            'upload_id',
            'face_image'
        ]



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
    property = forms.ModelChoiceField(
        queryset=Property.objects.all(),
        empty_label="Select Property",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tenant
        fields = ['name', 'email', 'phone', 'property', 'move_in_date', 'rent_amount', 'id_document', 'unit_number']
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: only show properties with available units
        self.fields['property'].queryset = Property.objects.all()



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'amount', 'expense_date', 'description']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'amount', 'expense_date', 'description']
