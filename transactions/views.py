from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone

from .models import Transaction
from categories.models import Category
from goals.models import SavingsGoal
from .forms import TransactionForm


@login_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # All calculations are scoped to the logged-in user
    user_transactions = Transaction.objects.filter(user=request.user)

    total_income = user_transactions.filter(
        type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses = user_transactions.filter(
        type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expenses

    monthly_income = user_transactions.filter(
        type='income',
        date__gte=month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_expenses = user_transactions.filter(
        type='expense',
        date__gte=month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    recent_transactions = user_transactions.order_by('-date', '-created_at')[:5]

    top_categories = Category.objects.annotate(
        spent=Sum(
            'transaction__amount',
            filter=Q(transaction__type='expense', transaction__user=request.user)
        )
    ).filter(spent__isnull=False).order_by('-spent')[:5]

    active_goals = SavingsGoal.objects.filter(
        user=request.user,
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


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)

    filter_type = request.GET.get('type')
    if filter_type in ['income', 'expense']:
        transactions = transactions.filter(type=filter_type)

    sort = request.GET.get('sort', '-date')
    if sort in ['date', '-date', 'amount', '-amount']:
        transactions = transactions.order_by(sort)

    context = {
        'transactions': transactions,
        'current_filter': filter_type,
        'current_sort': sort,
    }
    return render(request, 'transactions/transaction_list.html', context)


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'transactions/transaction_detail.html', {'transaction': transaction})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, f'Transaction "{transaction.title}" added successfully!')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm()

    return render(request, 'transactions/transaction_form.html', {
        'form': form,
        'title': 'Add Transaction'
    })


@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

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


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction
    })


@login_required
def transaction_by_type(request, transaction_type):
    transactions = Transaction.objects.filter(user=request.user, type=transaction_type)
    type_display = 'Income' if transaction_type == 'income' else 'Expenses'

    context = {
        'transactions': transactions,
        'type_display': type_display,
        'transaction_type': transaction_type,
    }
    return render(request, 'transactions/transaction_filter.html', context)
