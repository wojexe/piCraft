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
    image.save(tmp_file, format_img)
    # important because after save(), the fp is already at the end of the file
    tmp_file.seek(0)
    return tmp_file


class MyTestCase(APITestCase):
    def setUp(self):
        self.client = Client()

    def test_bad_request(self):
        uploaded_file = temporary_image()
        form_data = {
            "name": "resize",
            "height": "100",
            "width": "100",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resizee/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 404)

    def test_resize(self):
        uploaded_file = temporary_image()
        form_data = {
            "name": "resize",
            "height": "100",
            "width": "100",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/resize/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    def test_compress(self):
        uploaded_file = temporary_image()
        form_data = {
            "name": "compress",
            "rate": "50",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/compress/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    def test_enhance(self):
        uploaded_file = temporary_image()
        form_data = {
            "name": "enhance",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/enhance/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    def test_change_format(self):
        uploaded_file = temporary_image()
        form_data = {
            "name": "change_format",
            "format": "heic",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/change_format/"

        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)

    def test_combine(self):
        uploaded_file = temporary_image()
        form_data = {
            "params": """[
                {
                    "name": "resize",
                    "height": "100",
                    "width": "100"
                },
                {
                    "name": "compress",
                    "rate": "50"
                },
                {
                    "name": "enhance"
                },
                {
                    "name": "change_format",
                    "format": "heic"
                }
            ]""",
            "file": uploaded_file,
        }
        url = "http://127.0.0.1:8000/combine/"
        response = self.client.post(url, data=form_data, format="multipart")
        self.assertEqual(response.status_code, 200)
