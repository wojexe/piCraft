from parameterized import parameterized
import tempfile
from PIL import Image
from rest_framework.test import APITestCase
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.core.files.base import ContentFile
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile


def temporary_image(format_img="png"):
    """
    Returns a new temporary image file
    """

    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=f".{format_img}")
    image.save(tmp_file)
    # important because after save(), the fp is already at the end of the file
    tmp_file.seek(0)
    return tmp_file


class MyTestCase(APITestCase):
    def setUp(self):
        self.client = Client()


    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_height_small_resize(self, format):
        uploaded_file = temporary_image(format)

        form_data = {
            "params": """{"width": "330", "height": "2"}""",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_width_big_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": """{"width": "4332432", "height": "32"}""",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_not_integer_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": """{"width": "df", "height": "32"}""",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_good_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": """{"width": "330", "height": "32"}""",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    # compress

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_small_rate_compress(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": '{"rate": "3"}',
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/compress/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_big_rate_compress(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": '{"rate": "169"}',
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/compress/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_good_compress(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": '{"rate": "69"}',
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/compress/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    # enhance

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'),('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_good_enhance(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": """{}""",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/enhance/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    # change_format



    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_change_format_bad_format(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": '{"format": "pns"}',
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/change_format/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_change_format_good(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "params": '{"format": "png"}',
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/change_format/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)