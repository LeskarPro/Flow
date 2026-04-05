from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


@shared_task
def check_budget_alert(user_id):
    """
    Check if the user's monthly spending has crossed 80% of their budget limit.
    Triggered automatically after every transaction is saved.
    Sends an email alert if the threshold is reached.

    In local development the email is printed to the terminal
    (EMAIL_BACKEND = console). No real mail server needed.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    profile = getattr(user, 'profile', None)
    if not profile or not profile.monthly_budget_limit:
        return

    total_expenses = profile.get_total_expenses_this_month()
    limit = profile.monthly_budget_limit
    percentage = (total_expenses / limit) * 100

    if percentage >= 80:
        subject = f'[Flow] Budget alert — {percentage:.0f}% used this month'
        message = (
            f'Hi {user.username},\n\n'
            f'You have used {percentage:.1f}% of your monthly budget limit '
            f'({profile.currency} {total_expenses:.2f} of {profile.currency} {limit:.2f}).\n\n'
            f'Consider reviewing your expenses in Flow.\n\n'
            f'— The Flow Team'
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
