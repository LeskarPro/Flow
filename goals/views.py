from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import SavingsGoal
from .forms import SavingsGoalForm


def goal_list(request):
    # List all savings goals
    goals = SavingsGoal.objects.all()

    # Separate active and achieved goals
    active_goals = [g for g in goals if not g.is_achieved()]
    achieved_goals = [g for g in goals if g.is_achieved()]

    context = {
        'active_goals': active_goals,
        'achieved_goals': achieved_goals,
    }
    return render(request, 'goals/goal_list.html', context)


def goal_detail(request, pk):
    # View single savings goal
    goal = get_object_or_404(SavingsGoal, pk=pk)
    return render(request, 'goals/goal_detail.html', {'goal': goal})


def goal_create(request):
    # Create new savings goal
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save()
            messages.success(request, f'Goal "{goal.name}" created successfully!')
            return redirect('goal_detail', pk=goal.pk)
    else:
        form = SavingsGoalForm()

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'title': 'Create Savings Goal'
    })


def goal_edit(request, pk):
    # Edit existing savings goal
    goal = get_object_or_404(SavingsGoal, pk=pk)

    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully!')
            return redirect('goal_detail', pk=goal.pk)
    else:
        form = SavingsGoalForm(instance=goal)

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'goal': goal,
        'title': 'Edit Goal'
    })


def goal_delete(request, pk):
    # Delete goal with confirmation
    goal = get_object_or_404(SavingsGoal, pk=pk)

    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully!')
        return redirect('goal_list')

    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})