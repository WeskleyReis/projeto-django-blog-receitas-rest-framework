from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': 1}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe to test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': 1}
            )
        )
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn(needed_title, content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published is False dont show"""
        # Need a recipe to test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': recipe.category.id}
            )
        )
        self.assertEqual(response.status_code, 404)
