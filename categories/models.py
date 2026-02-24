from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    COLOR_CHOICES = [
        ('primary', 'Blue'),
        ('success', 'Green'),
        ('danger', 'Red'),
        ('warning', 'Yellow'),
        ('info', 'Light Blue'),
        ('secondary', 'Gray'),
        ('dark', 'Black'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Category name (e.g., Groceries, Rent, Salary)"
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Optional description of the category"
    )
    budget_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Monthly budget limit for this category"
    )
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='primary',
        help_text="Color for UI display"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def total_spent(self):
        # Calculate total spent in this category
        return self.transaction_set.filter(
            type='expense'
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    def budget_remaining(self):
        # Calculate remaining budget
        return self.budget_limit - self.total_spent()

    def budget_percentage(self):
        # Calculate percentage of budget used
        if self.budget_limit > 0:
            return (self.total_spent() / self.budget_limit) * 100
        return 0

    def clean(self):
        if self.budget_limit <= 0:
            raise ValidationError({'budget_limit': 'Budget limit must be greater than zero'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)