from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from categories.models import Category
from transactions.models import Transaction


def make_category(name='Test Category', budget_limit=300):
    return Category.objects.create(name=name, budget_limit=budget_limit)


class CategoryListViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='catuser', password='pass123')

    def test_list_accessible_to_logged_in_user(self):
        self.client.login(username='catuser', password='pass123')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_redirects_anonymous_user(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])


class CategoryDetailViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='detailuser', password='pass123')
        self.other = User.objects.create_user(username='otheruser', password='pass123')
        self.category = make_category()

    def test_detail_shows_only_current_users_transactions(self):
        # Create one transaction for self.user and one for other
        Transaction.objects.create(
            title='My expense',
            amount=10,
            date=date.today(),
            type='expense',
            category=self.category,
            user=self.user,
        )
        Transaction.objects.create(
            title='Their expense',
            amount=20,
            date=date.today(),
            type='expense',
            category=self.category,
            user=self.other,
        )
        self.client.login(username='detailuser', password='pass123')
        response = self.client.get(
            reverse('category_detail', kwargs={'pk': self.category.pk})
        )
        self.assertContains(response, 'My expense')
        self.assertNotContains(response, 'Their expense')
