from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from categories.models import Category
from transactions.models import Transaction, Tag


def make_category(name='Food', budget_limit=500):
    return Category.objects.create(name=name, budget_limit=budget_limit)


def make_transaction(user, title='Groceries', amount=50, tx_type='expense', category=None):
    if tx_type == 'expense' and category is None:
        category = make_category(name=f'Cat-{title}')
    return Transaction.objects.create(
        title=title,
        amount=amount,
        date=date.today(),
        type=tx_type,
        category=category,
        user=user,
    )


class TransactionListViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='txuser', password='pass123')

    def test_list_requires_login(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_list_shows_own_transactions_only(self):
        other = User.objects.create_user(username='other', password='pass123')
        make_transaction(self.user, title='Mine')
        make_transaction(other, title='Theirs')
        self.client.login(username='txuser', password='pass123')
        response = self.client.get(reverse('transaction_list'))
        self.assertContains(response, 'Mine')
        self.assertNotContains(response, 'Theirs')


class TransactionCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='pass123')
        self.category = make_category()
        self.client.login(username='creator', password='pass123')

    def test_create_assigns_logged_in_user(self):
        self.client.post(reverse('transaction_create'), {
            'title': 'Lunch',
            'amount': '12.50',
            'date': date.today().isoformat(),
            'type': 'expense',
            'category': self.category.pk,
        })
        tx = Transaction.objects.filter(title='Lunch').first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.user, self.user)


class TransactionEditDeleteTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass123')
        self.other = User.objects.create_user(username='stranger', password='pass123')
        self.tx = make_transaction(self.user)

    def test_edit_other_users_transaction_returns_404(self):
        self.client.login(username='stranger', password='pass123')
        response = self.client.get(
            reverse('transaction_edit', kwargs={'pk': self.tx.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_requires_post_confirmation(self):
        self.client.login(username='owner', password='pass123')
        # GET should show confirmation page, not delete
        response = self.client.get(
            reverse('transaction_delete', kwargs={'pk': self.tx.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Transaction.objects.filter(pk=self.tx.pk).exists())


class TransactionModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='modeluser', password='pass123')
        self.category = make_category()

    def test_expense_without_category_raises_validation_error(self):
        from django.core.exceptions import ValidationError
        tx = Transaction(
            title='Bad expense',
            amount=10,
            date=date.today(),
            type='expense',
            category=None,
            user=self.user,
        )
        with self.assertRaises(ValidationError):
            tx.full_clean()

    def test_formatted_amount_property(self):
        expense = make_transaction(self.user, tx_type='expense', amount=Decimal('42.00'))
        income = make_transaction(self.user, title='Salary', tx_type='income', amount=Decimal('1000.00'))
        self.assertEqual(expense.formatted_amount, '-$42.00')
        self.assertEqual(income.formatted_amount, '$1000.00')
