from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from categories.models import Category
from transactions.models import Transaction


def make_category(name='API Category', budget_limit=500):
    return Category.objects.create(name=name, budget_limit=budget_limit)


def make_transaction(user, title='Test TX', amount=50):
    category = make_category(name=f'Cat-{title}')
    return Transaction.objects.create(
        title=title,
        amount=amount,
        date=date.today(),
        type='expense',
        category=category,
        user=user,
    )


class TransactionAPIAuthTests(TestCase):

    def test_unauthenticated_request_returns_403(self):
        response = self.client.get(reverse('api_transaction_list'))
        self.assertEqual(response.status_code, 403)


class TransactionAPIListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='pass123')
        self.other = User.objects.create_user(username='apiother', password='pass123')
        self.client.login(username='apiuser', password='pass123')

    def test_authenticated_returns_only_own_transactions(self):
        make_transaction(self.user, title='My TX')
        make_transaction(self.other, title='Other TX')
        response = self.client.get(reverse('api_transaction_list'))
        self.assertEqual(response.status_code, 200)
        titles = [tx['title'] for tx in response.json()]
        self.assertIn('My TX', titles)
        self.assertNotIn('Other TX', titles)

    def test_post_creates_transaction_for_logged_in_user(self):
        category = make_category(name='Dining')
        response = self.client.post(
            reverse('api_transaction_list'),
            data={
                'title': 'Restaurant',
                'amount': '35.00',
                'date': date.today().isoformat(),
                'type': 'expense',
                'category_id': category.pk,
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        tx = Transaction.objects.filter(title='Restaurant').first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.user, self.user)
