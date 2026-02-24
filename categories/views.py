from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Category
from transactions.models import Transaction
from .forms import CategoryForm


def category_list(request):
    # List all categories with their budget stats
    categories = Category.objects.all()

    # Add spent amount to each category
    for category in categories:
        category.spent = Transaction.objects.filter(
            category=category,
            type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {'categories': categories}
    return render(request, 'categories/category_list.html', context)


def category_detail(request, pk):
    # View single category with its transactions
    category = get_object_or_404(Category, pk=pk)

    # Get transactions for this category
    transactions = Transaction.objects.filter(category=category).order_by('-date')

    # Calculate stats
    total_spent = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'category': category,
        'transactions': transactions,
        'total_spent': total_spent,
        'total_income': total_income,
    }
    return render(request, 'categories/category_detail.html', context)


def category_create(request):
    # Create new category
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


def category_edit(request, pk):
    # Edit existing category
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


def category_delete(request, pk):
    # Delete category with confirmation
    category = get_object_or_404(Category, pk=pk)

    # Check if category has transactions
    has_transactions = Transaction.objects.filter(category=category).exists()

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')

    return render(request, 'categories/category_confirm_delete.html', {
        'category': category,
        'has_transactions': has_transactions
    })