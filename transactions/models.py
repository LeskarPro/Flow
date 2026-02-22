from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from categories.models import Category
import datetime


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    title = models.CharField(
        max_length=100,
        help_text="Short description of the transaction"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Transaction amount (positive number)"
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Date of transaction"
    )
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        default='expense',
        help_text="Income or expense"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Category for this transaction"
    )
    description = models.TextField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Additional details about the transaction"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.get_type_display()})"

    def clean(self):
        # Validate date is not in future
        if self.date > timezone.now().date():
            raise ValidationError({'date': 'Transaction date cannot be in the future'})

        # Validate category for expense transactions
        if self.type == 'expense' and not self.category:
            raise ValidationError({'category': 'Expense transactions must have a category'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def formatted_amount(self):
        """Return amount with sign based on transaction type"""
        if self.type == 'expense':
            return f"-${self.amount}"
        return f"${self.amount}"