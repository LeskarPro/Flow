from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator


class Profile(models.Model):
    """Extended user profile with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    monthly_budget_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Monthly budget limit for expenses"
    )
    currency = models.CharField(
        max_length=3,
        default='EUR',
        choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('BGN', 'BGN')]
    )
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_total_expenses_this_month(self):
        """Calculate total expenses for current month"""
        from django.utils import timezone
        from transactions.models import Transaction

        now = timezone.now()
        return Transaction.objects.filter(
            user=self.user,
            type='expense',
            date__year=now.year,
            date__month=now.month
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    def get_remaining_budget(self):
        """Calculate remaining monthly budget"""
        if self.monthly_budget_limit:
            return self.monthly_budget_limit - self.get_total_expenses_this_month()
        return None

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile when user is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Auto-save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()