from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from utils.img_recize import img_recize
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext as _
from tag.models import Tag
from django.forms import ValidationError
from collections import defaultdict


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name
    

class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id')


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True, blank=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation Time'))
    preparation_time_unit = models.CharField(max_length=65, verbose_name=_('Time Unit'))
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(max_length=65, verbose_name=_('Serving Unit'))
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    def save(self, *args, **kwargs):
        # Automatically generate slug if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.title)

        current_cover = self.cover.name
        saved = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            try:
                img_recize(self.cover)
            except FileNotFoundError:
                pass

        return saved
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')