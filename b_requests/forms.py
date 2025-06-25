from django import forms
from .models import BorrowRequest, ReturnRequest
from django.utils import timezone
import datetime


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['date_requested', 'return_date']
        widgets = {
            'date_requested': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border border-gray-300 rounded p-2 w-full'
            }),
            'return_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border border-gray-300 rounded p-2 w-full'
            }),
        }

    def __init__(self, *args, min_date=None, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.min_date = min_date or today

        # Apply dynamic min and initial values
        self.fields['date_requested'].widget.attrs['min'] = self.min_date.isoformat()
        self.fields['return_date'].widget.attrs['min'] = self.min_date.isoformat()
        self.fields['date_requested'].initial = self.min_date
        self.fields['return_date'].required = True

    def clean(self):
        cleaned_data = super().clean()
        date_requested = cleaned_data.get('date_requested')
        return_date = cleaned_data.get('return_date')

        if date_requested:
            if isinstance(date_requested, datetime.datetime):
                date_requested = date_requested.date()

            if date_requested < self.min_date:
                self.add_error('date_requested', f'Date must be on or after {self.min_date}.')

        if return_date and date_requested and return_date < date_requested:
            self.add_error('return_date', 'Return date must be after the request date.')


class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['condition', 'feedback']
        widgets = {
            'condition': forms.Select(attrs={
                'class': 'border border-gray-300 rounded p-2 w-full'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'border border-gray-300 rounded p-2 w-full',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['condition'].required = True
