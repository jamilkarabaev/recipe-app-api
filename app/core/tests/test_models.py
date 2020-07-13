from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """"test creating a new user with email is successful"""
        email = 'test@londonappdev.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test email for new user is normalized"""
        email = 'test@LONDONAPPDEV.com'
        user = get_user_model().objects.create_user(email=email,password='123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test that creating user without email raises error"""

        """If value error is raised, it passes, if no value error raised, it fails"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_super_user('superuser','12345')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)