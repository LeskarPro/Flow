from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Transaction
from categories.models import Category
from goals.models import SavingsGoal
from .forms import TransactionForm


# Dashboard with summary statistics and recent data
def dashboard(request):
    # Get current month date range
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Calculate totals
    total_income = Transaction.objects.filter(
        type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses = Transaction.objects.filter(
        type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expenses

    # Monthly totals
    monthly_income = Transaction.objects.filter(
        type='income',
        date__gte=month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_expenses = Transaction.objects.filter(
        type='expense',
        date__gte=month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Recent transactions
    recent_transactions = Transaction.objects.all()[:5]

    # Top spending categories
    top_categories = Category.objects.annotate(
        spent=Sum('transaction__amount',
                  filter=Q(transaction__type='expense'))
    ).filter(spent__isnull=False).order_by('-spent')[:5]

    # Active goals
    active_goals = SavingsGoal.objects.filter(
        deadline__gte=today
    )[:3]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'recent_transactions': recent_transactions,
        'top_categories': top_categories,
        'active_goals': active_goals,
    }
    return render(request, 'transactions/dashboard.html', context)


def transaction_list(request):
    # List all transactions
    transactions = Transaction.objects.all()

    # Filter by type if specified
    filter_type = request.GET.get('type')
    if filter_type in ['income', 'expense']:
        transactions = transactions.filter(type=filter_type)

    # Sort by
    sort = request.GET.get('sort', '-date')
    if sort in ['date', '-date', 'amount', '-amount']:
        transactions = transactions.order_by(sort)

    context = {
        'transactions': transactions,
        'current_filter': filter_type,
        'current_sort': sort,
    }
    return render(request, 'transactions/transaction_list.html', context)


def transaction_detail(request, pk):
    # View single transaction
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transactions/transaction_detail.html', {'transaction': transaction})


def transaction_create(request):
    # Create new transaction
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            messages.success(request, f'Transaction "{transaction.title}" created successfully!')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm()

    return render(request, 'transactions/transaction_form.html', {
        'form': form,
        'title': 'Add Transaction'
    })


def transaction_edit(request, pk):
    # Edit existing transaction
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transactions/transaction_form.html', {
        'form': form,
        'transaction': transaction,
        'title': 'Edit Transaction'
    })


def transaction_delete(request, pk):
    # Delete transaction with confirmation
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction
    })


def transaction_by_type(request, transaction_type):
    # Filter transactions by type
    transactions = Transaction.objects.filter(type=transaction_type)
    type_display = 'Income' if transaction_type == 'income' else 'Expenses'

    context = {
        'transactions': transactions,
        'type_display': type_display,
        'transaction_type': transaction_type,
    }
    return render(request, 'transactions/transaction_filter.html', context)