from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient, Recipe
from recipe import serializers
from rest_framework.decorators import action 
from rest_framework.response import Response

class BaseRecipeAttr(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base Viewset for user owned recipe attrs"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        assigned_only = bool(int(self.request.query_params.get('assigned_only', 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    """Manage Tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseRecipeAttr):
    """Manage Ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def _params_to_ints(self, qs):
        """Convert a list of string id's to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Override our current stated queryset to only display self.request.users recipes from the db table"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)


        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer_class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """After validation with other fields, simply adds user when saving to dbase table"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






        


    
    



