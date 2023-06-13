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
    def test_bad_name_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "name": "resiz e",
            "height": "100",
            "width": "100",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_height_small_resize(self, format):
        uploaded_file = temporary_image(format)

        form_data = {
            "name": "resize",
            "height": "1",
            "width": "100",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_width_big_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "name": "resize",
            "height": "100",
            "width": 100000,
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_bad_not_integer_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "name": "resize",
            "height": "dsa",
            "width": "100",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    def test_good_resize(self, format):
        uploaded_file = temporary_image(format)
        form_data = {
            "name": "resize",
            "height": "100",
            "width": "100",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    # @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    # def test_bad_file_resize(self, format):
    #     uploaded_file = temporary_image(format)
    #     form_data = {
    #         "name": "resize",
    #         "height": "100",
    #         "width": "100",
    #         "file": uploaded_file,
    #     }
    #     url = "http://127.0.0.1:8000/resize/"

    #     response = self.client.post(url, data=form_data, format="multipart")
    #     self.assertEqual(response.status_code, 200)
    
    # @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    # def test_bad_format_resize(self, format):
    #     uploaded_file = temporary_image(format)
    #     form_data = {
    #         "name": "resize",
    #         "height": "100",
    #         "width": "100",
    #         "file": uploaded_file,
    #     }
    #     url = "http://127.0.0.1:8000/resize/"

    #     response = self.client.post(url, data=form_data, format="multipart")
    #     self.assertEqual(response.status_code, 200)

    # @parameterized.expand([('jpg'), ('jpeg'), ('png'), ('heic'), ('gif'), ('tiff'), ('bmp'), ('webp')])
    # def test_bad_form_data(self, format):
    #     uploaded_file = temporary_image(format)
    #     form_data = {
    #         "name": "resize",
    #         "height": "100",
    #         "width": "100",
    #         "file": uploaded_file,
    #     }
    #     url = "http://127.0.0.1:8000/resize/"

    #     response = self.client.post(url, data=form_data, format="multipart")
    #     self.assertEqual(response.status_code, 200)
