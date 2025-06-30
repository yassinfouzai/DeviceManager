from django import forms
from .models import BorrowRequest, ReturnRequest
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['date_requested', 'return_date']
        widgets = {
            'date_requested': forms.TextInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'flatpickr w-full p-2 rounded-[8px] bg-white text-[16px] text-atb-g-500 border border-atb-g-300 placeholder-atb-g-500 hover:text-atb-g-900 focus:text-atb-g-900 focus:ring-atb-p-200 focus:border-atb-p-200 focus:outline-none transition duration-200',
                'autocomplete': 'off',  # optional, prevents autofill UI interference
            }),
            'return_date': forms.TextInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'flatpickr w-full p-2 rounded-[8px] bg-white text-[16px] text-atb-g-500 border border-atb-g-300 placeholder-atb-g-500 hover:text-atb-g-900 focus:text-atb-g-900 focus:ring-atb-p-200 focus:border-atb-p-200 focus:outline-none transition duration-200',
                'autocomplete': 'off',
            }),
        }

    def __init__(self, *args, min_date=None, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.min_date = min_date or today

        self.fields['date_requested'].widget.attrs['min'] = self.min_date.isoformat()
        self.fields['return_date'].widget.attrs['min'] = self.min_date.isoformat()
        self.fields['date_requested'].initial = self.min_date
        self.fields['return_date'].required = True

    def clean(self):
        cleaned_data = super().clean()
        date_requested = cleaned_data.get('date_requested')
        return_date = cleaned_data.get('return_date')

        if date_requested and isinstance(date_requested, datetime.datetime):
            date_requested = date_requested.date()

        if date_requested and date_requested < self.min_date:
            self.add_error('date_requested', f'Date must be on or after {self.min_date}.')

        if date_requested and return_date:
            if return_date < date_requested:
                self.add_error('return_date', 'Return date must be after the request date.')

            device = self.instance.device
            if device:
                overlap_exists = BorrowRequest.objects.filter(
                    device=device,
                    approved=True,
                    date_requested__lte=return_date,
                    return_date__gte=date_requested
                ).exists()

                if overlap_exists:
                    raise forms.ValidationError("This device is already reserved during the selected period.")

        return cleaned_data



class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['condition', 'feedback']
        widgets = {
            'condition': forms.Select(attrs={
            'class': (
            'w-full py-2 pr-8 pl-4 rounded-[8px] bg-white text-[16px] text-atb-g-900 '
            'border border-atb-g-300 placeholder-atb-g-500 hover:text-atb-g-900 '
            'focus:text-atb-g-900 focus:ring-atb-p-200 focus:border-atb-p-200 '
            'focus:outline-none focus:shadow-[0_0_0_4px_#FDE3E6] '
                )
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded-[8px] bg-white text-[16px] text-atb-g-500 border border-atb-g-300 placeholder-atb-g-500 hover:text-atb-g-900 hover:text-atb-g-900 focus:text-atb-g-900 focus:ring-atb-p-200 focus:border-atb-p-200 focus:outline-none focus:shadow-[0_0_0_4px_#FDE3E6] transition duration-200',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['condition'].required = True
