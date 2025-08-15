from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Category'),
            author=self.make_author(username='newuser'),
            title='Test Recipe',
            description='Test Description',
            slug='test-recipe',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=2,
            servings_unit='People',
            preparation_steps='Test Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg = 'Recipe preparation_steps_is_html is not False'
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg = 'Recipe is_published is not False'
        )

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe),
            'Testing Representation',
            msg=f'Recipe string representation must be "{needed}" but "{str(self.recipe)}" was received.'
        )

    def test_recipe_save_calls_img_recize(self):
        from unittest.mock import patch
        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image
        import io

        # Create an image in memory
        image = Image.new('RGB', (1200, 600), color='red')
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        django_image = SimpleUploadedFile(
            name='test_cover.jpg',
            content=img_bytes.read(),
            content_type='image/jpeg'
        )

        with patch('recipes.models.img_recize') as mock_img_recize:
            self.recipe.cover = django_image
            self.recipe.save()
            # Check if img_recize was called
            mock_img_recize.assert_called_once()

    def test_recipe_slug_generate_dont_exist(self):
        self.recipe.title = 'Test for slug in recipe'
        self.recipe.slug = ''
        self.recipe.save()
        self.assertEqual('test-for-slug-in-recipe', self.recipe.slug)
