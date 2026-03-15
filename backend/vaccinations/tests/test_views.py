from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta

from pets.models import Pet
from vaccinations.models import Vaccination

User = get_user_model()


class VaccinationViewSetTestCase(TestCase):
    """疫苗记录测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='vactest',
            password='TestPassword123!',
            email='vac@example.com'
        )
        self.client.force_authenticate(user=self.user)

        # 创建宠物
        self.pet = Pet.objects.create(
            owner=self.user,
            name='测试宠物',
            species='dog'
        )

        self.vaccinations_url = '/api/vaccinations/'

        # 创建疫苗记录
        self.vaccination = Vaccination.objects.create(
            pet=self.pet,
            vaccine_name='狂犬疫苗',
            vaccination_date=date(2024, 1, 15),
            next_due_date=date(2025, 1, 15),
            clinic='宠物医院',
            doctor='张医生'
        )

    def test_get_vaccination_list(self):
        """测试获取疫苗列表"""
        response = self.client.get(self.vaccinations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vaccination_detail(self):
        """测试获取疫苗详情"""
        response = self.client.get(f'{self.vaccinations_url}{self.vaccination.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vaccine_name'], '狂犬疫苗')

    def test_create_vaccination(self):
        """测试创建疫苗记录"""
        data = {
            'pet': self.pet.id,
            'vaccine_name': '犬瘟热疫苗',
            'vaccination_date': '2024-03-01',
            'next_due_date': '2025-03-01',
            'clinic': '宠物诊所',
            'doctor': '李医生'
        }
        response = self.client.post(self.vaccinations_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_vaccination(self):
        """测试更新疫苗记录"""
        data = {
            'vaccine_name': '狂犬疫苗（更新）',
            'clinic': '新医院'
        }
        response = self.client.patch(f'{self.vaccinations_url}{self.vaccination.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vaccination.refresh_from_db()
        self.assertEqual(self.vaccination.vaccine_name, '狂犬疫苗（更新）')

    def test_delete_vaccination(self):
        """测试删除疫苗记录"""
        response = self.client.delete(f'{self.vaccinations_url}{self.vaccination.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vaccination.objects.filter(id=self.vaccination.id).exists())


class VaccinationFilterTestCase(TestCase):
    """疫苗筛选测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='vacfiltertest',
            password='TestPassword123!',
            email='vacfilter@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.pet = Pet.objects.create(owner=self.user, name='测试宠物', species='dog')
        self.vaccinations_url = '/api/vaccinations/'

        # 创建不同日期的疫苗记录
        Vaccination.objects.create(
            pet=self.pet,
            vaccine_name='疫苗1',
            vaccination_date=date(2024, 1, 1),
            next_due_date=date(2024, 6, 1)
        )
        Vaccination.objects.create(
            pet=self.pet,
            vaccine_name='疫苗2',
            vaccination_date=date(2024, 3, 1),
            next_due_date=date(2024, 9, 1)
        )

    def test_filter_by_pet(self):
        """测试按宠物筛选"""
        response = self.client.get(f'{self.vaccinations_url}?pet_id={self.pet.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)