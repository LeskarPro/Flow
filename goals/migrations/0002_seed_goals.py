from django.db import migrations
from django.utils import timezone
from datetime import timedelta

# Create initial savings goals with data and links to a category
def create_initial_goals(apps, schema_editor):
    SavingsGoal = apps.get_model('goals', 'SavingsGoal')
    Category = apps.get_model('categories', 'Category')

    today = timezone.now().date()

    # Get categories
    vacation_categories = Category.objects.filter(name__in=['Transportation', 'Dining Out', 'Entertainment'])
    laptop_categories = Category.objects.filter(name__in=['Shopping', 'Freelance'])
    emergency_categories = Category.objects.filter(name__in=['Healthcare', 'Groceries'])

    goals = [
        {
            'name': 'Summer Vacation Fund',
            'target_amount': 2000.00,
            'current_amount': 750.00,
            'deadline': today + timedelta(days=90),
            'notes': 'Trip to the mountains in June',
        },
        {
            'name': 'New Laptop',
            'target_amount': 1500.00,
            'current_amount': 450.00,
            'deadline': today + timedelta(days=60),
            'notes': 'MacBook Air for development work',
        },
        {
            'name': 'Emergency Fund',
            'target_amount': 5000.00,
            'current_amount': 2100.00,
            'deadline': today + timedelta(days=180),
            'notes': '3 months of expenses covered',
        },
        {
            'name': 'New Smartphone',
            'target_amount': 800.00,
            'current_amount': 200.00,
            'deadline': today + timedelta(days=45),
            'notes': 'Saving for iPhone/Pixel',
        },
        {
            'name': 'Christmas Gifts',
            'target_amount': 600.00,
            'current_amount': 100.00,
            'deadline': today + timedelta(days=270),
            'notes': 'Budget for holiday gifts',
        },
    ]

    for goal_data in goals:
        goal = SavingsGoal.objects.create(**goal_data)

        # Add M2M relationships based on goal name
        if goal.name == 'Summer Vacation Fund':
            goal.categories.set(vacation_categories)
        elif goal.name == 'New Laptop':
            goal.categories.set(laptop_categories)
        elif goal.name == 'Emergency Fund':
            goal.categories.set(emergency_categories)


def remove_initial_goals(apps, schema_editor):
    SavingsGoal = apps.get_model('goals', 'SavingsGoal')
    SavingsGoal.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('goals', '0001_initial'),  # Adjust based on your actual initial migration
        ('categories', '0002_seed_categories'),  # Reference the categories seed migration
    ]

    operations = [
        migrations.RunPython(create_initial_goals, remove_initial_goals),
    ]