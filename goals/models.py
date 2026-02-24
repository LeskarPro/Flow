from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from categories.models import Category


class SavingsGoal(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Name of your savings goal (e.g., New Laptop, Vacation)"
    )
    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1.00)],
        help_text="Total amount you want to save"
    )
    current_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Amount saved so far"
    )
    deadline = models.DateField(
        help_text="Target date to achieve this goal"
    )
    notes = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Additional notes about this goal"
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        help_text="Categories that contribute to this goal"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['deadline', 'name']

    def __str__(self):
        return f"{self.name} (${self.current_amount}/${self.target_amount})"

    def progress_percentage(self):
        # Calculate progress percentage
        if self.target_amount > 0:
            return min((self.current_amount / self.target_amount) * 100, 100)
        return 0

    def remaining_amount(self):
        # Calculate amount left to save
        return max(self.target_amount - self.current_amount, 0)

    def days_remaining(self):
        # Calculate days until deadline
        if self.deadline >= timezone.now().date():
            return (self.deadline - timezone.now().date()).days
        return 0

    def is_achieved(self):
        # Check if goal is achieved
        return self.current_amount >= self.target_amount

    def clean(self):
        if self.deadline <= timezone.now().date():
            raise ValidationError({'deadline': 'Deadline must be in the future'})

        if self.current_amount > self.target_amount:
            raise ValidationError({
                'current_amount': 'Current amount cannot exceed target amount'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)