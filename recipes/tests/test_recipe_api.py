from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixing
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(test.APITestCase, RecipeMixing):
    def get_recipe_api_list(self):
        return self.client.get(reverse('recipes:recipes-api-list'))

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_load_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_bath(qtd=wanted_number_of_recipes)
        response = self.get_recipe_api_list()
        qtd_of_loaded_recipes = len(response.data.get('results'))
        self.assertEqual(wanted_number_of_recipes, qtd_of_loaded_recipes)

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_bath(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )
