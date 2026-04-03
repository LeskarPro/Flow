from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
        }),
        label='Email Address',
        help_text='We will use this for account notifications.',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repeat your password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your password',
        })
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'


class ProfileUpdateForm(forms.ModelForm):
    # First name and last name from the User model
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}),
        label='First Name',
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}),
        label='Last Name',
    )

    class Meta:
        model = Profile
        fields = ['currency', 'monthly_budget_limit', 'email_notifications']
        widgets = {
            'monthly_budget_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2000.00',
                'step': '0.01',
            }),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'currency': 'Preferred Currency',
            'monthly_budget_limit': 'Monthly Budget Limit',
            'email_notifications': 'Enable Email Notifications',
        }
        help_texts = {
            'monthly_budget_limit': 'Leave blank if you do not want a monthly spending limit.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Currency is read-only once set — you cannot change it after your first save
        if self.instance.pk and self.instance.currency:
            self.fields['currency'].disabled = True
            self.fields['currency'].help_text = 'Currency cannot be changed after it is set.'
        else:
            self.fields['currency'].widget.attrs.update({'class': 'form-select'})

        # Pre-fill first/last name from the related user
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Also save first/last name back to the User model
        profile.user.first_name = self.cleaned_data.get('first_name', '')
        profile.user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            profile.user.save()
            profile.save()
        return profile
