from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """用户注册测试"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'

    def test_user_registration_success(self):
        """测试用户注册成功"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!',
            'nickname': '测试用户',
            'phone': '13800138000'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_password_mismatch(self):
        """测试密码不匹配"""
        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'TestPassword123!',
            'password_confirm': 'DifferentPassword123!',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_username(self):
        """测试重复用户名"""
        User.objects.create_user(username='existinguser', password='TestPassword123!')
        data = {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(TestCase):
    """用户登录测试"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login/'
        self.user = User.objects.create_user(
            username='logintest',
            password='TestPassword123!',
            email='login@example.com'
        )

    def test_user_login_success(self):
        """测试登录成功"""
        data = {
            'username': 'logintest',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_user_login_wrong_password(self):
        """测试密码错误"""
        data = {
            'username': 'logintest',
            'password': 'WrongPassword123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_nonexistent_user(self):
        """测试用户不存在"""
        data = {
            'username': 'nonexistent',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTestCase(TestCase):
    """用户资料测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='profiletest',
            password='TestPassword123!',
            nickname='测试昵称',
            email='profile@example.com'
        )
        self.profile_url = '/api/user/profile/'

    def test_get_profile_authenticated(self):
        """测试获取已认证用户资料"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profiletest')

    def test_get_profile_unauthenticated(self):
        """测试获取未认证用户资料"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """测试更新用户资料"""
        self.client.force_authenticate(user=self.user)
        data = {'nickname': '新昵称', 'phone': '13900139000'}
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, '新昵称')


class ChangePasswordTestCase(TestCase):
    """修改密码测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='passwordtest',
            password='OldPassword123!',
            email='password@example.com'
        )
        self.password_url = '/api/user/password/'

    def test_change_password_success(self):
        """测试修改密码成功"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'OldPassword123!',
            'new_password': 'NewPassword123!'
        }
        response = self.client.put(self.password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!'))

    def test_change_password_wrong_old(self):
        """测试原密码错误"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'WrongPassword123!',
            'new_password': 'NewPassword123!'
        }
        response = self.client.put(self.password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)