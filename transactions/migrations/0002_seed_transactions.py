from django.db import migrations
from django.utils import timezone
from datetime import timedelta
import random


def create_initial_transactions(apps, schema_editor):
    Transaction = apps.get_model('transactions', 'Transaction')
    Category = apps.get_model('categories', 'Category')

    # Get categories
    categories = {
        'Salary': Category.objects.get(name='Salary'),
        'Freelance': Category.objects.get(name='Freelance'),
        'Groceries': Category.objects.get(name='Groceries'),
        'Rent': Category.objects.get(name='Rent'),
        'Utilities': Category.objects.get(name='Utilities'),
        'Transportation': Category.objects.get(name='Transportation'),
        'Dining Out': Category.objects.get(name='Dining Out'),
        'Entertainment': Category.objects.get(name='Entertainment'),
        'Shopping': Category.objects.get(name='Shopping'),
        'Healthcare': Category.objects.get(name='Healthcare'),
    }

    today = timezone.now().date()

    transactions = [
        # Income transactions
        {
            'title': 'Monthly Salary - March',
            'amount': 4500.00,
            'date': today - timedelta(days=5),
            'type': 'income',
            'category': categories['Salary'],
            'description': 'March 2026 salary payment'
        },
        {
            'title': 'Freelance Website Project',
            'amount': 850.00,
            'date': today - timedelta(days=12),
            'type': 'income',
            'category': categories['Freelance'],
            'description': 'Payment for client website development'
        },
        {
            'title': 'Bonus Payment',
            'amount': 500.00,
            'date': today - timedelta(days=5),
            'type': 'income',
            'category': categories['Salary'],
            'description': 'Performance bonus'
        },
        {
            'title': 'Freelance Design Work',
            'amount': 350.00,
            'date': today - timedelta(days=25),
            'type': 'income',
            'category': categories['Freelance'],
            'description': 'Logo design for local business'
        },

        # Expense transactions
        {
            'title': 'Monthly Rent',
            'amount': 1200.00,
            'date': today - timedelta(days=1),
            'type': 'expense',
            'category': categories['Rent'],
            'description': 'March rent payment'
        },
        {
            'title': 'Electricity Bill',
            'amount': 85.50,
            'date': today - timedelta(days=10),
            'type': 'expense',
            'category': categories['Utilities'],
            'description': 'February electricity bill'
        },
        {
            'title': 'Water Bill',
            'amount': 45.30,
            'date': today - timedelta(days=10),
            'type': 'expense',
            'category': categories['Utilities'],
            'description': 'February water bill'
        },
        {
            'title': 'Internet & Cable',
            'amount': 79.99,
            'date': today - timedelta(days=8),
            'type': 'expense',
            'category': categories['Utilities'],
            'description': 'Monthly internet subscription'
        },
        {
            'title': 'Weekly Groceries',
            'amount': 156.47,
            'date': today - timedelta(days=3),
            'type': 'expense',
            'category': categories['Groceries'],
            'description': 'Walmart - weekly groceries'
        },
        {
            'title': 'Gas Station',
            'amount': 45.00,
            'date': today - timedelta(days=2),
            'type': 'expense',
            'category': categories['Transportation'],
            'description': 'Filled gas tank'
        },
        {
            'title': 'Dinner at Italian Restaurant',
            'amount': 78.50,
            'date': today - timedelta(days=6),
            'type': 'expense',
            'category': categories['Dining Out'],
            'description': 'Date night dinner'
        },
        {
            'title': 'Cinema Tickets',
            'amount': 32.00,
            'date': today - timedelta(days=9),
            'type': 'expense',
            'category': categories['Entertainment'],
            'description': 'Movie tickets for 2'
        },
        {
            'title': 'New Running Shoes',
            'amount': 89.99,
            'date': today - timedelta(days=14),
            'type': 'expense',
            'category': categories['Shopping'],
            'description': 'Nike running shoes'
        },
        {
            'title': 'Pharmacy',
            'amount': 35.75,
            'date': today - timedelta(days=4),
            'type': 'expense',
            'category': categories['Healthcare'],
            'description': 'Vitamins and medicine'
        },
        {
            'title': 'Coffee Shops',
            'amount': 24.50,
            'date': today - timedelta(days=1),
            'type': 'expense',
            'category': categories['Dining Out'],
            'description': 'Various coffee purchases'
        },
        {
            'title': 'Uber Rides',
            'amount': 32.50,
            'date': today - timedelta(days=7),
            'type': 'expense',
            'category': categories['Transportation'],
            'description': 'Uber rides this week'
        },
    ]

    for transaction_data in transactions:
        Transaction.objects.create(**transaction_data)


def remove_initial_transactions(apps, schema_editor):
    Transaction = apps.get_model('transactions', 'Transaction')
    Transaction.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0001_initial'),  # Adjust based on your actual initial migration
        ('categories', '0002_seed_categories'),  # Reference the categories seed migration
    ]

    operations = [
        migrations.RunPython(create_initial_transactions, remove_initial_transactions),
    ]