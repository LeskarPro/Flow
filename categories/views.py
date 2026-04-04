from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Category
from .forms import CategoryForm
from transactions.models import Transaction


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Annotate each category with how much the current user has spent in it
        return Category.objects.annotate(
            spent=Sum(
                'transaction__amount',
                filter=Q(transaction__type='expense', transaction__user=self.request.user)
            )
        ).order_by('name')


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.filter(
            category=self.object,
            user=self.request.user
        ).order_by('-date')
        context['transactions'] = transactions
        context['total_spent'] = (
            transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        )
        context['total_income'] = (
            transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        )
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Category'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Category'
        context['category'] = self.object
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_transactions'] = Transaction.objects.filter(
            category=self.object,
            user=self.request.user
        ).exists()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Category deleted successfully!')
        return super().form_valid(form)
