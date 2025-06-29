from django import forms
from .models import Reservation, RoomType
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    destination = forms.CharField(required=False, label="Destination")
    name = forms.CharField(required=False, label="Hotel Name")

    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Check-in Date"
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Check-out Date"
    )

    adults = forms.ChoiceField(
        choices=[(i, f"{i} Adult{'s' if i > 1 else ''}") for i in range(1, 5)],
        label="Adults"
    )
    children = forms.ChoiceField(
        choices=[(i, f"{i} Child{'ren' if i != 1 else ''}") for i in range(0, 5)],
        label="Children"
    )
    infants = forms.ChoiceField(
        choices=[(i, f"{i} Infant{'s' if i != 1 else ''}") for i in range(0, 3)],
        label="Infants"
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out']

    def __init__(self, *args, **kwargs):
        self.room_type = kwargs.pop('room_type', None)
        readonly = kwargs.pop('readonly', False)
        super().__init__(*args, **kwargs)

        self.fields['check_in'].widget.attrs.update({'type': 'date'})
        self.fields['check_out'].widget.attrs.update({'type': 'date'})

        if readonly:
            self.fields['check_in'].widget.attrs['readonly'] = True
            self.fields['check_out'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if not self.room_type:
            raise forms.ValidationError("Room type must be specified.")
        if not check_in or not check_out:
            raise forms.ValidationError("Check-in and check-out dates are required.")
        if check_in >= check_out:
            raise forms.ValidationError("Check-out must be after check-in.")

        # Assign to the instance
        self.instance.room_type = self.room_type
        self.instance.check_in = check_in
        self.instance.check_out = check_out

        # No quantity restriction — we allow overbooking now
        return cleaned_data

