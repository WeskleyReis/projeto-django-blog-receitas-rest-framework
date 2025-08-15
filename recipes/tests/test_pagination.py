from django.test import TestCase
from recipes.models import Recipe
from django.urls import reverse
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def setUp(self):
        # Create 10 dummy recipes for testing
        recipes = [
            Recipe(
                title=f'Recipe {i}',
                slug=f'recipe-{i}',
                description='Description',
                preparation_time=10,
                preparation_time_unit='Minutes',
                servings=5,
                servings_unit='People',
                preparation_steps='Steps',
                is_published=True,
            ) for i in range(10)
        ]
        Recipe.objects.bulk_create(recipes)

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=2,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=3,
        )
        self.assertEqual([2, 3, 4, 5], pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=4,
        )
        self.assertEqual([3, 4, 5, 6], pagination['pagination'])

    def test_pagination_invalid_page_returns_404(self):
        url = reverse('recipes:home')
        response = self.client.get(f'{url}?page=999')
        self.assertEqual(response.status_code, 404)