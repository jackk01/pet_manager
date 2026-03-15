from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from pets.models import Pet

User = get_user_model()


class PetViewSetTestCase(TestCase):
    """宠物管理测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='pettest',
            password='TestPassword123!',
            email='pet@example.com'
        )
        self.client.force_authenticate(user=self.user)
        self.pets_url = '/api/pets/'

        # 创建测试宠物
        self.pet = Pet.objects.create(
            owner=self.user,
            name='测试宠物',
            species='dog',
            breed='金毛',
            gender='male',
            birth_date='2020-01-01'
        )

    def test_get_pet_list(self):
        """测试获取宠物列表"""
        response = self.client.get(self.pets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pet_detail(self):
        """测试获取宠物详情"""
        response = self.client.get(f'{self.pets_url}{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], '测试宠物')

    def test_create_pet(self):
        """测试创建宠物"""
        data = {
            'name': '新宠物',
            'species': 'cat',
            'breed': '波斯猫',
            'gender': 'female',
            'birth_date': '2021-06-01'
        }
        response = self.client.post(self.pets_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Pet.objects.filter(name='新宠物').exists())

    def test_update_pet(self):
        """测试更新宠物"""
        data = {'name': '更新后的宠物名称', 'breed': '萨摩耶'}
        response = self.client.put(f'{self.pets_url}{self.pet.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.name, '更新后的宠物名称')

    def test_delete_pet_soft_delete(self):
        """测试软删除宠物"""
        response = self.client.delete(f'{self.pets_url}{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pet.refresh_from_db()
        self.assertFalse(self.pet.is_active)

    def test_create_pet_without_auth(self):
        """测试未认证创建宠物"""
        self.client.logout()
        data = {'name': '新宠物', 'species': 'dog'}
        response = self.client.post(self.pets_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PetFilterTestCase(TestCase):
    """宠物筛选测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='filtertest',
            password='TestPassword123!',
            email='filter@example.com'
        )
        self.client.force_authenticate(user=self.user)
        self.pets_url = '/api/pets/'

        # 创建不同类型的宠物
        Pet.objects.create(owner=self.user, name='狗狗1', species='dog', is_active=True)
        Pet.objects.create(owner=self.user, name='猫咪1', species='cat', is_active=True)
        Pet.objects.create(owner=self.user, name='已删除的宠物', species='dog', is_active=False)

    def test_filter_by_species(self):
        """测试按物种筛选"""
        response = self.client.get(f'{self.pets_url}?species=dog')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_default_excludes_inactive(self):
        """测试默认不包含已删除的宠物"""
        response = self.client.get(self.pets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 应该只返回活跃的宠物
        for pet in response.data['results']:
            self.assertTrue(pet['is_active'])