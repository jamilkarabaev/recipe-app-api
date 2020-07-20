from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.adminuser = get_user_model().objects.create_super_user(email='superuser1@gmail.com',password='123')
        self.client.force_login(self.adminuser)
        self.user = get_user_model().objects.create_user(email='user1@gmail.com', password='123', name='user')

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """Test that editing users works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that adding users on the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)



    



        

