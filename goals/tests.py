from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from goals.models import SavingsGoal


def future_date(days=30):
    return date.today() + timedelta(days=days)


class SavingsGoalModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='goaluser', password='pass123')

    def test_progress_percentage_calculation(self):
        goal = SavingsGoal(
            name='Holiday',
            target_amount=1000,
            current_amount=250,
            deadline=future_date(60),
            user=self.user,
        )
        self.assertAlmostEqual(goal.progress_percentage(), 25.0)

    def test_progress_percentage_capped_at_100(self):
        goal = SavingsGoal(
            name='Exceeded Goal',
            target_amount=100,
            current_amount=100,
            deadline=future_date(60),
            user=self.user,
        )
        self.assertEqual(goal.progress_percentage(), 100.0)


class GoalCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='creategoal', password='pass123')
        self.client.login(username='creategoal', password='pass123')

    def test_create_assigns_logged_in_user(self):
        self.client.post(reverse('goal_create'), {
            'name': 'New Laptop',
            'target_amount': '1200.00',
            'current_amount': '0',
            'deadline': future_date(90).isoformat(),
        })
        goal = SavingsGoal.objects.filter(name='New Laptop').first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.user, self.user)
