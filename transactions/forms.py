from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Transaction, Tag


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'date', 'type', 'category', 'description', 'tags']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Add any notes...'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Transaction Title',
            'amount': 'Amount ($)',
            'type': 'Transaction Type',
            'category': 'Category',
            'tags': 'Tags',
        }
        help_texts = {
            'amount': 'Enter a positive number (e.g., 50.00)',
            'tags': 'Optional — select one or more tags to label this transaction.',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.date < timezone.now().date():
            self.fields['date'].disabled = True
            self.fields['date'].help_text = 'Date cannot be changed for past transactions'

        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g., Grocery shopping'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': '0.00'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].empty_label = "--- Select a category (required for expenses) ---"
        self.fields['description'].required = False
        self.fields['tags'].required = False

        # Filter tags to only show the current user's tags
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)
        else:
            self.fields['tags'].queryset = Tag.objects.none()

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

        if transaction_type == 'expense' and not category:
            raise ValidationError({
                'category': 'Expense transactions must have a category. Please select one.'
            })

        return cleaned_data


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        labels = {
            'name': 'Tag Name',
            'color': 'Badge Colour',
        }
        help_texts = {
            'name': 'Short label, e.g. "tax-deductible" or "one-off".',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g. tax-deductible',
        })
        self.fields['color'].widget.attrs.update({'class': 'form-select'})
