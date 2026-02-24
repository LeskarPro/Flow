from django import forms
from .models import Transaction
from django.core.exceptions import ValidationError
from django.utils import timezone


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'date', 'type', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Add any notes...'}),
        }
        labels = {
            'title': 'Transaction Title',
            'amount': 'Amount ($)',
            'type': 'Transaction Type',
            'category': 'Category',
        }
        help_texts = {
            'amount': 'Enter a positive number (e.g., 50.00)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # READ-ONLY FIELD: Date becomes read-only if editing an old transaction
        if self.instance.pk and self.instance.date < timezone.now().date():
            self.fields['date'].disabled = True
            self.fields['date'].help_text = 'Date cannot be changed for past transactions'

        # Customize all fields with Bootstrap classes
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g., Grocery shopping'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': '0.00'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].empty_label = "--- Select a category (required for expenses) ---"

        # EXCLUDED FIELDS: description is excluded in some cases? No, we keep it but make it optional
        self.fields['description'].required = False

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError('Amount must be greater than zero')
        return amount

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise ValidationError('Transaction date cannot be in the future')
        return date

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        category = cleaned_data.get('category')

        # Custom validation: expense must have category
        if transaction_type == 'expense' and not category:
            raise ValidationError({
                'category': 'Expense transactions must have a category. Please select one.'
            })

        return cleaned_data