from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date

from pets.models import Pet
from health_records.models import HealthRecord

User = get_user_model()


class HealthRecordViewSetTestCase(TestCase):
    """健康记录测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='healthtest',
            password='TestPassword123!',
            email='health@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.pet = Pet.objects.create(
            owner=self.user,
            name='测试宠物',
            species='dog'
        )

        self.health_url = '/api/health-records/'

        self.health_record = HealthRecord.objects.create(
            pet=self.pet,
            record_type='体检',
            title='年度体检',
            record_date=date(2024, 1, 15),
            hospital='宠物医院',
            doctor='张医生',
            diagnosis='健康',
            cost=200.00
        )

    def test_get_health_record_list(self):
        """测试获取健康记录列表"""
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_health_record_detail(self):
        """测试获取健康记录详情"""
        response = self.client.get(f'{self.health_url}{self.health_record.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '年度体检')

    def test_create_health_record(self):
        """测试创建健康记录"""
        data = {
            'pet': self.pet.id,
            'record_type': '就诊',
            'title': '感冒就诊',
            'record_date': '2024-03-01',
            'hospital': '宠物诊所',
            'doctor': '李医生',
            'diagnosis': '感冒',
            'cost': 150.00
        }
        response = self.client.post(self.health_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_health_record(self):
        """测试更新健康记录"""
        data = {'title': '年度体检（更新）', 'diagnosis': '健康状况良好'}
        response = self.client.patch(f'{self.health_url}{self.health_record.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.health_record.refresh_from_db()
        self.assertEqual(self.health_record.title, '年度体检（更新）')

    def test_delete_health_record(self):
        """测试删除健康记录"""
        response = self.client.delete(f'{self.health_url}{self.health_record.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HealthRecord.objects.filter(id=self.health_record.id).exists())

    def test_filter_by_record_type(self):
        """测试按记录类型筛选"""
        response = self.client.get(f'{self.health_url}?record_type=体检')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HealthRecordModelTestCase(TestCase):
    """健康记录模型测试"""

    def setUp(self):
        self.user = User.objects.create_user(username='modeltest', password='TestPassword123!')
        self.pet = Pet.objects.create(owner=self.user, name='测试宠物', species='dog')

    def test_health_record_creation(self):
        """测试健康记录创建"""
        record = HealthRecord.objects.create(
            pet=self.pet,
            record_type='手术',
            title='绝育手术',
            record_date=date(2024, 2, 1),
            cost=800.00
        )
        self.assertEqual(record.title, '绝育手术')
        self.assertEqual(record.record_type, '手术')
        self.assertEqual(record.cost, 800.00)