from django import forms
from .models import Tenant

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'  # Or list fields explicitly

    # Ensure correct file input handling
    photo = forms.ImageField(required=False)
    id_document = forms.FileField(required=False)
