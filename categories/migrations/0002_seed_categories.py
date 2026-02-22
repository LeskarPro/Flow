from django.db import migrations


def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')

    categories = [
        {
            'name': 'Salary',
            'description': 'Monthly income from work',
            'budget_limit': 5000.00,
            'color': 'success'
        },
        {
            'name': 'Freelance',
            'description': 'Side projects and freelance work',
            'budget_limit': 2000.00,
            'color': 'info'
        },
        {
            'name': 'Groceries',
            'description': 'Food and household items',
            'budget_limit': 600.00,
            'color': 'primary'
        },
        {
            'name': 'Rent',
            'description': 'Monthly rent payment',
            'budget_limit': 1200.00,
            'color': 'danger'
        },
        {
            'name': 'Utilities',
            'description': 'Electricity, water, internet',
            'budget_limit': 300.00,
            'color': 'warning'
        },
        {
            'name': 'Transportation',
            'description': 'Gas, public transport, maintenance',
            'budget_limit': 200.00,
            'color': 'secondary'
        },
        {
            'name': 'Dining Out',
            'description': 'Restaurants and cafes',
            'budget_limit': 250.00,
            'color': 'orange'
        },
        {
            'name': 'Entertainment',
            'description': 'Movies, games, hobbies',
            'budget_limit': 150.00,
            'color': 'purple'
        },
        {
            'name': 'Shopping',
            'description': 'Clothes, electronics, other purchases',
            'budget_limit': 300.00,
            'color': 'dark'
        },
        {
            'name': 'Healthcare',
            'description': 'Medical expenses, pharmacy',
            'budget_limit': 200.00,
            'color': 'info'
        },
    ]

    for category_data in categories:
        Category.objects.create(**category_data)


def remove_initial_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('categories', '0001_initial'),  # Adjust based on your actual initial migration
    ]

    operations = [
        migrations.RunPython(create_initial_categories, remove_initial_categories),
    ]