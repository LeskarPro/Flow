from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task
def check_goal_deadlines():
    """
    Periodic task — runs every day at 8:00 AM (configured in CELERY_BEAT_SCHEDULE).
    Finds all unachieved savings goals with a deadline within the next 7 days
    and sends a reminder email to each goal's owner.

    In local development the email is printed to the terminal
    (EMAIL_BACKEND = console). No real mail server needed.
    """
    from goals.models import SavingsGoal

    today = timezone.now().date()
    deadline_cutoff = today + timedelta(days=7)

    upcoming_goals = SavingsGoal.objects.filter(
        deadline__gte=today,
        deadline__lte=deadline_cutoff,
        user__isnull=False,
    ).select_related('user', 'user__profile')

    for goal in upcoming_goals:
        if goal.is_achieved():
            continue

        user = goal.user
        days_left = (goal.deadline - today).days
        remaining = goal.remaining_amount()

        try:
            currency = user.profile.currency
        except Exception:
            currency = 'EUR'

        subject = f'[Flow] Reminder: "{goal.name}" deadline in {days_left} day(s)'
        message = (
            f'Hi {user.username},\n\n'
            f'Your savings goal "{goal.name}" is due in {days_left} day(s) '
            f'({goal.deadline}).\n\n'
            f'Progress: {currency} {goal.current_amount:.2f} / {currency} {goal.target_amount:.2f} '
            f'({goal.progress_percentage():.0f}% complete)\n'
            f'Still needed: {currency} {remaining:.2f}\n\n'
            f'Keep it up!\n\n'
            f'— The Flow Team'
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
