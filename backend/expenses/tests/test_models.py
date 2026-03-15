# Statistics tests - using Django's test client
# Statistics views don't have traditional model tests as they are aggregate queries

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date

from pets.models import Pet
from vaccinations.models import Vaccination
from health_records.models import HealthRecord
from expenses.models import Expense

User = get_user_model()


class StatisticsViewTestCase(TestCase):
    """统计数据测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='statstest',
            password='TestPassword123!',
            email='stats@example.com'
        )
        self.client.force_authenticate(user=self.user)

        # 创建测试数据
        self.pet = Pet.objects.create(
            owner=self.user,
            name='测试宠物',
            species='dog'
        )

        Vaccination.objects.create(
            pet=self.pet,
            vaccine_name='狂犬疫苗',
            vaccination_date=date(2024, 1, 1)
        )

        HealthRecord.objects.create(
            pet=self.pet,
            record_type='体检',
            title='年度体检',
            record_date=date(2024, 1, 15),
            cost=200.00
        )

        Expense.objects.create(
            pet=self.pet,
            category='食品',
            amount=150.00,
            expense_date=date(2024, 1, 15)
        )

    def test_dashboard_statistics(self):
        """测试仪表盘统计数据"""
        response = self.client.get('/api/statistics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pet_count', response.data)
        self.assertIn('total_expense', response.data)

    def test_expense_statistics(self):
        """测试消费统计"""
        response = self.client.get('/api/statistics/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('by_category', response.data)