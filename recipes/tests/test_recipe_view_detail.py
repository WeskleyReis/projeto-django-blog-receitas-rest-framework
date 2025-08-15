from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=[1]))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:recipe', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        # Need a recipe to test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        """Test recipe is_published is False dont show"""
        # Need a recipe to test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:recipe',
            args=(recipe.id,)
            )
        )
        self.assertEqual(response.status_code, 404)
