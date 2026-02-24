from django import forms
from .models import SavingsGoal
from django.core.exceptions import ValidationError
from django.utils import timezone


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'current_amount', 'deadline', 'notes', 'categories']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Add any notes...'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }
        labels = {
            'name': 'Goal Name',
            'target_amount': 'Target Amount ($)',
            'current_amount': 'Current Savings ($)',
            'deadline': 'Target Date',
            'categories': 'Related Categories',
        }
        help_texts = {
            'deadline': 'When do you want to achieve this goal?',
            'categories': 'Hold Ctrl/Cmd to select multiple',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.is_achieved():
            self.fields['current_amount'].disabled = True
            self.fields['current_amount'].help_text = 'Goal achieved! Amount cannot be changed.'

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g., Summer Vacation'})
        self.fields['target_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': '2000.00'})
        self.fields['current_amount'].widget.attrs.update({'class': 'form-control', 'placeholder': '0.00'})

        self.fields['notes'].required = False

    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get('target_amount')
        current = cleaned_data.get('current_amount')
        deadline = cleaned_data.get('deadline')

        if target and current and current > target:
            raise ValidationError({
                'current_amount': 'Current savings cannot exceed target amount'
            })

        if deadline and deadline <= timezone.now().date():
            raise ValidationError({
                'deadline': 'Deadline must be in the future'
            })

        return cleaned_data