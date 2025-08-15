from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()
    
    def test_category_string_representation(self):
        needed = 'Testing Representation'
        self.category.name = 'Testing Representation'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category),
            'Testing Representation',
            msg=f'Category string represatiton must be "{needed}" but "{str(self.category)}" was received.'
        )
    
    def test_category_name_max_lenght_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
