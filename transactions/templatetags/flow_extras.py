from django import template
from django.template.defaultfilters import stringfilter
from transactions.models import Transaction
from django.db.models import Sum

register = template.Library()

@register.filter
def currency(value):
    """Format value as currency"""
    try:
        return f"${value:,.2f}"
    except (TypeError, ValueError):
        return "$0.00"

@register.filter
def progress_percentage(value, total):
    """Calculate progress percentage"""
    try:
        if total and total > 0:
            return min(int((value / total) * 100), 100)
        return 0
    except (TypeError, ValueError, ZeroDivisionError):
        return 0

@register.simple_tag
def total_income():
    """Get total income from all transactions"""
    total = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum']
    return total or 0

@register.simple_tag
def total_expenses():
    """Get total expenses from all transactions"""
    total = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum']
    return total or 0

@register.filter
def days_until(date):
    """Calculate days until a given date"""
    from django.utils import timezone
    if date:
        delta = date - timezone.now().date()
        return delta.days
    return 0