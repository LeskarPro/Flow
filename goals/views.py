from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import SavingsGoal
from .forms import SavingsGoalForm


class GoalListView(LoginRequiredMixin, ListView):
    model = SavingsGoal
    template_name = 'goals/goal_list.html'

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goals = self.get_queryset()
        context['active_goals'] = [g for g in goals if not g.is_achieved()]
        context['achieved_goals'] = [g for g in goals if g.is_achieved()]
        return context


class GoalDetailView(LoginRequiredMixin, DetailView):
    model = SavingsGoal
    template_name = 'goals/goal_detail.html'
    context_object_name = 'goal'

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = 'goals/goal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Savings Goal'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Goal "{form.instance.name}" created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('goal_detail', kwargs={'pk': self.object.pk})


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = 'goals/goal_form.html'

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Goal'
        context['goal'] = self.object
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Goal updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('goal_detail', kwargs={'pk': self.object.pk})


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingsGoal
    template_name = 'goals/goal_confirm_delete.html'
    context_object_name = 'goal'
    success_url = reverse_lazy('goal_list')

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Goal deleted successfully!')
        return super().form_valid(form)
