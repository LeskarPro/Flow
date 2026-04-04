from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView,
)

from .models import Transaction, Tag
from .forms import TransactionForm, TagForm
from categories.models import Category
from goals.models import SavingsGoal


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        month_start = today.replace(day=1)
        user = self.request.user

        user_transactions = Transaction.objects.filter(user=user)

        total_income = user_transactions.filter(
            type='income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_expenses = user_transactions.filter(
            type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        monthly_income = user_transactions.filter(
            type='income', date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        monthly_expenses = user_transactions.filter(
            type='expense', date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        top_categories = Category.objects.annotate(
            spent=Sum(
                'transaction__amount',
                filter=Q(transaction__type='expense', transaction__user=user)
            )
        ).filter(spent__isnull=False).order_by('-spent')[:5]

        context.update({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'recent_transactions': user_transactions.order_by('-date', '-created_at')[:5],
            'top_categories': top_categories,
            'active_goals': SavingsGoal.objects.filter(
                user=user, deadline__gte=today
            )[:3],
        })
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        filter_type = self.request.GET.get('type')
        if filter_type in ['income', 'expense']:
            queryset = queryset.filter(type=filter_type)
        sort = self.request.GET.get('sort', '-date')
        if sort in ['date', '-date', 'amount', '-amount']:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('type')
        context['current_sort'] = self.request.GET.get('sort', '-date')
        return context


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Transaction'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Transaction "{form.instance.title}" added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transaction_detail', kwargs={'pk': self.object.pk})


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Transaction'
        context['transaction'] = self.object
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Transaction updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transaction_detail', kwargs={'pk': self.object.pk})


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Transaction deleted successfully!')
        return super().form_valid(form)


class TransactionByTypeView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_filter.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user,
            type=self.kwargs['transaction_type']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = self.kwargs['transaction_type']
        context['type_display'] = 'Income' if t == 'income' else 'Expenses'
        context['transaction_type'] = t
        return context


# --- Tag views ---

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'transactions/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'transactions/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Tag'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Tag "{form.instance.name}" created!')
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'transactions/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Tag'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tag updated!')
        return super().form_valid(form)


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'transactions/tag_confirm_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('tag_list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Tag deleted.')
        return super().form_valid(form)
