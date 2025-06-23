from django import forms
from .models import Reservation, Room
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
        fields = ['guest_name', 'guest_email', 'check_in', 'check_out']

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        readonly = kwargs.pop('readonly', False)  # Optional: make fields readonly
        super().__init__(*args, **kwargs)

        # Set input types for better UI (calendar picker)
        self.fields['check_in'].widget.attrs.update({'type': 'date'})
        self.fields['check_out'].widget.attrs.update({'type': 'date'})

        if readonly:
            self.fields['check_in'].widget.attrs['readonly'] = True
            self.fields['check_out'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        if self.room is None:
            raise forms.ValidationError("Room must be specified.")
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if not check_in or not check_out:
            raise forms.ValidationError("Check-in and check-out dates are required.")
        self.instance.room = self.room
        self.instance.check_in = check_in
        self.instance.check_out = check_out
        try:
            self.instance.clean()
        except ValidationError as e:
            raise forms.ValidationError(
                e.message_dict if hasattr(e, 'message_dict') else e.messages
        )
        return cleaned_data
