from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date

from pets.models import Pet
from expenses.models import Expense

User = get_user_model()


class ExpenseViewSetTestCase(TestCase):
    """消费记录测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='expensetest',
            password='TestPassword123!',
            email='expense@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.pet = Pet.objects.create(
            owner=self.user,
            name='测试宠物',
            species='dog'
        )

        self.expenses_url = '/api/expenses/'

        self.expense = Expense.objects.create(
            pet=self.pet,
            category='食品',
            amount=150.00,
            expense_date=date(2024, 1, 15),
            description='狗粮',
            payment_method='alipay'
        )

    def test_get_expense_list(self):
        """测试获取消费列表"""
        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expense_detail(self):
        """测试获取消费详情"""
        response = self.client.get(f'{self.expenses_url}{self.expense.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '150.00')

    def test_create_expense(self):
        """测试创建消费记录"""
        data = {
            'pet': self.pet.id,
            'category': '医疗',
            'amount': 300.00,
            'expense_date': '2024-03-01',
            'description': '疫苗',
            'payment_method': 'wechat'
        }
        response = self.client.post(self.expenses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_expense(self):
        """测试更新消费记录"""
        data = {'amount': 200.00, 'description': '更新后的描述'}
        response = self.client.patch(f'{self.expenses_url}{self.expense.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(float(self.expense.amount), 200.00)

    def test_delete_expense(self):
        """测试删除消费记录"""
        response = self.client.delete(f'{self.expenses_url}{self.expense.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

    def test_filter_by_category(self):
        """测试按分类筛选"""
        response = self.client.get(f'{self.expenses_url}?category=食品')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_pet(self):
        """测试按宠物筛选"""
        response = self.client.get(f'{self.expenses_url}?pet_id={self.pet.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ExpenseModelTestCase(TestCase):
    """消费记录模型测试"""

    def setUp(self):
        self.user = User.objects.create_user(username='modeltest', password='TestPassword123!')
        self.pet = Pet.objects.create(owner=self.user, name='测试宠物', species='dog')

    def test_expense_creation(self):
        """测试消费记录创建"""
        expense = Expense.objects.create(
            pet=self.pet,
            category='玩具',
            amount=50.00,
            expense_date=date(2024, 2, 1),
            description='球'
        )
        self.assertEqual(expense.category, '玩具')
        self.assertEqual(float(expense.amount), 50.00)