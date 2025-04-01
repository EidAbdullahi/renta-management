from django import forms
from .models import Tenant
from django import forms
from .models import Payment, Tenant

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
