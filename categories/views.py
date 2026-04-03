from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q

from .models import Category
from transactions.models import Transaction
from .forms import CategoryForm


@login_required
def category_list(request):
    categories = Category.objects.all()

    for category in categories:
        category.spent = Transaction.objects.filter(
            category=category,
            type='expense',
            user=request.user
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {'categories': categories}
    return render(request, 'categories/category_list.html', context)


@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Show only the logged-in user's transactions for this category
    transactions = Transaction.objects.filter(
        category=category,
        user=request.user
    ).order_by('-date')

    total_spent = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'category': category,
        'transactions': transactions,
        'total_spent': total_spent,
        'total_income': total_income,
    }
    return render(request, 'categories/category_detail.html', context)


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()

    return render(request, 'categories/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/category_form.html', {
        'form': form,
        'category': category,
        'title': 'Edit Category'
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    has_transactions = Transaction.objects.filter(category=category, user=request.user).exists()

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')

    return render(request, 'categories/category_confirm_delete.html', {
        'category': category,
        'has_transactions': has_transactions
    })
