from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from utils.img_recize import img_recize
from PIL import Image
import io
from pathlib import Path
from django.conf import settings

class ImgRecizeTest(TestCase):
    def setUp(self):
        # Create a image in memory for testing
        self.img_width = 1200
        self.img_height = 600
        self.img_format = 'JPEG'
        self.img_name = 'test_image.jpg'
        image = Image.new('RGB', (self.img_width, self.img_height), color='red')
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=self.img_format)
        img_bytes.seek(0)
        self.django_image = SimpleUploadedFile(
            name=self.img_name,
            content=img_bytes.read(),
            content_type='image/jpeg'
        )
        # Save a image in MEDIA_ROOT to simulate real upload
        media_path = Path(settings.MEDIA_ROOT) / self.img_name
        with open(media_path, 'wb') as f:
            f.write(self.django_image.read())
        self.django_image.seek(0)

    def tearDown(self):
        # Remove the created image after the test
        media_path = Path(settings.MEDIA_ROOT) / self.img_name
        if media_path.exists():
            media_path.unlink()

    def test_img_recize_reduces_width(self):
        # Test a if the image is resized corretly
        new_width = 800
        img_recize(self.django_image, new_width=new_width)
        media_path = Path(settings.MEDIA_ROOT) / self.img_name
        with Image.open(media_path) as img:
            self.assertEqual(img.width, new_width)
            expected_height = round(new_width * self.img_height / self.img_width)
            self.assertEqual(img.height, expected_height)

    def test_img_recize_does_not_resize_smaller_images(self):
        # Test a if images smaller than the limit are not resized
        small_width = 400
        small_height = 200
        image = Image.new('RGB', (small_width, small_height), color='blue')
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=self.img_format)
        img_bytes.seek(0)
        small_image = SimpleUploadedFile(
            name='small_image.jpg',
            content=img_bytes.read(),
            content_type='image/jpeg'
        )
        media_path = Path(settings.MEDIA_ROOT) / 'small_image.jpg'
        with open(media_path, 'wb') as f:
            f.write(small_image.read())
        small_image.seek(0)
        result = img_recize(small_image, new_width=800)
        with Image.open(media_path) as img:
            self.assertEqual(img.width, small_width)
            self.assertEqual(img.height, small_height)
        if media_path.exists():
            media_path.unlink()

    def test_img_recize_returns_new_image_object(self):
        # Test if the function returns a PIL.Image.Image object
        result = img_recize(self.django_image, new_width=800)
        self.assertTrue(hasattr(result, 'size'))
        self.assertEqual(result.width, 800)