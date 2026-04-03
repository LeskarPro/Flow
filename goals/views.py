from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import SavingsGoal
from .forms import SavingsGoalForm


@login_required
def goal_list(request):
    goals = SavingsGoal.objects.filter(user=request.user)

    active_goals = [g for g in goals if not g.is_achieved()]
    achieved_goals = [g for g in goals if g.is_achieved()]

    context = {
        'active_goals': active_goals,
        'achieved_goals': achieved_goals,
    }
    return render(request, 'goals/goal_list.html', context)


@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    return render(request, 'goals/goal_detail.html', {'goal': goal})


@login_required
def goal_create(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            form.save_m2m()  # Save the ManyToMany categories field
            messages.success(request, f'Goal "{goal.name}" created successfully!')
            return redirect('goal_detail', pk=goal.pk)
    else:
        form = SavingsGoalForm()

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'title': 'Create Savings Goal'
    })


@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)

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


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)

    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully!')
        return redirect('goal_list')

    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})
