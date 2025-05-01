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
from .models import VacantRoom,ForSaleProperty, CommercialProperty
from .models import Profile

from django import forms
from .models import Employee
from .models import Property
from .models import Partner

# forms.py

from django import forms


class VacantRoomForm(forms.ModelForm):
    class Meta:
        model = VacantRoom
        fields = '__all__'
        exclude = ['user']



class VacancySearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search by title or location')
    room_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(VacantRoom.ROOM_TYPE_CHOICES),
        required=False
    )
    min_price = forms.DecimalField(required=False, label='Min Price')
    max_price = forms.DecimalField(required=False, label='Max Price')
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
        user = kwargs.pop('user', None)
        super(TenantForm, self).__init__(*args, **kwargs)

        if user is not None:
            self.fields['property'].queryset = Property.objects.filter(user=user)
        if not self.fields['property'].queryset.exists():
            self.fields['property'].empty_label = "No properties available. Please add one."





class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'amount', 'expense_date', 'description', 'receipt']









from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserRegisterForm(UserCreationForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Pending approval

        # Temporarily storing full_name and phone_number in first_name and last_name for demo purposes
        user.first_name = self.cleaned_data['full_name']
        user.last_name = self.cleaned_data['phone_number']

        if commit:
            user.save()
        return user
# (Optional) custom login form to show friendlier message for inactive accounts
class InactiveUserAuthForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "inactive": "Your account is pending approval by an administrator.",
    }





class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'image']





class EmployeeSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search by Name')
    position = forms.ChoiceField(
        required=False,
        choices=[('', 'Filter by Position'), 
                 ('Manager', 'Manager'), 
                 ('Developer', 'Developer'), 
                 ('Designer', 'cleaner')],
        label='Position'
    )


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'website']




class ForSalePropertyForm(forms.ModelForm):
    class Meta:
        model = ForSaleProperty
        fields = '__all__'

class CommercialPropertyForm(forms.ModelForm):
    class Meta:
        model = CommercialProperty
        fields = '__all__'