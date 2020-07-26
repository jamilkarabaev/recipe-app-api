from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientsApiTests(TestCase):
    """Test the publically availible ingredients api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the login is required for this endpoint"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    

class PrivateIngredientsApiTests(TestCase):
    """Test that the privately availible ingredients api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('jamil.karabaev@gmail.com', '123')
        self.client.force_authenticate(self.user)

    
    def test_retrieve_ingredients_list(self):
        """Test retrieving list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENTS_URL)
        ings = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_ingredients_limited_to_user(self):
        """Test that the ingredients are limited to the specific user"""
        user = get_user_model().objects.create_user('test@gmail.com', '154')
        Ingredient.objects.create(user=user, name='Kale')
        selfusering = Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], selfusering.name)
