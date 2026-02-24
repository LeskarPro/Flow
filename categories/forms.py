from django import forms
from .models import Category
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'budget_limit', 'color']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Optional description...'}),
        }
        labels = {
            'name': 'Category Name',
            'budget_limit': 'Monthly Budget Limit ($)',
            'color': 'Display Color',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g., Groceries'})
        self.fields['budget_limit'].widget.attrs.update({'class': 'form-control', 'placeholder': '500.00'})

        self.fields['color'].widget = forms.Select(choices=Category.COLOR_CHOICES, attrs={'class': 'form-select'})

        self.fields['description'].required = False

    def clean_budget_limit(self):
        budget = self.cleaned_data['budget_limit']
        if budget <= 0:
            raise ValidationError('Budget limit must be greater than zero')
        return budget

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError('Category name must be at least 3 characters long')
        return name