from PIL import Image
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PhotoSerializer
from .models import Image as ImageClass
import imghdr
from django.http import FileResponse
from . import utils as us

# Create your views here.
LEGAL_FORMATS = ['jpg', 'jpeg', 'png', 'gifv', 'heic', 'gif', 'tiff', 'bmp', 'webp']


class Resize(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # todo: more validation data?
            # todo: logic for Resizing
            file_serializer = PhotoSerializer(data=request.data)
            name = request.data['name']
            width = request.data['width']
            height = request.data['height']
            width_image = int(width)
            height_image = int(height)
            if file_serializer.is_valid() and name == 'resize' and width_image > 0 and height_image > 0 and imghdr.what(
                    file_serializer.validated_data['file']) in LEGAL_FORMATS:
                instance = file_serializer.save()
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s)
                # to do check response Content-Type
                # resp.set_headers({'Content-Type': 'multipart/form-data'})
                # resp['Content-Type'] = 'multipart/form-data'
                return resp
            else:
                return Response(file_serializer.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)


class Compress(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # todo: more validation data?
            # todo: logic for Compressing
            file_serializer = PhotoSerializer(data=request.data)
            name = request.data['name']
            rate = request.data['rate']
            rate_image = int(rate)
            if file_serializer.is_valid() and name == 'compress' and 0 <= rate_image <= 100 and imghdr.what(
                    file_serializer.validated_data['file']) in LEGAL_FORMATS:
                instance = file_serializer.save()
                s = open(instance.file.path, 'rb')

                resp = FileResponse(s)
                # to do check response Content-Type
                # resp.set_headers({'Content-Type': 'multipart/form-data'})
                # resp['Content-Type'] = 'multipart/form-data'
                return resp
            else:
                return Response(file_serializer.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)


class Enhance(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # todo: more validation data?
            # todo: logic for Enhancing
            file_serializer = PhotoSerializer(data=request.data)
            name = request.data['name']
            if file_serializer.is_valid() and name == 'enhance' and imghdr.what(
                    file_serializer.validated_data['file']) in LEGAL_FORMATS:
                instance = file_serializer.save()
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s)
                # to do check response Content-Type
                # resp.set_headers({'Content-Type': 'multipart/form-data'})
                # resp['Content-Type'] = 'multipart/form-data'

                return resp
            else:
                return Response(file_serializer.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)


class ChangeFormat(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # todo: more validation data?
            # todo: logic for ChangingFormat
            file_serializer = PhotoSerializer(data=request.data)
            name = request.data['name']
            format_image = request.data['format']
            if file_serializer.is_valid() and name == 'enhance' and imghdr.what(
                    file_serializer.validated_data['file']) in LEGAL_FORMATS and format_image in LEGAL_FORMATS:
                instance = file_serializer.save()
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s)
                # to do check response Content-Type
                # resp.set_headers({'Content-Type': 'multipart/form-data'})
                # resp['Content-Type'] = 'multipart/form-data'

                return resp
            else:
                return Response(file_serializer.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)


class Combine(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # todo: more validation data?
            # todo: logic for ChangingFormat
            file_serializer = PhotoSerializer(data=request.data)
            name = request.data['name']
            operations = request.data['operations']

            if file_serializer.is_valid() and name == 'enhance' and imghdr.what(
                    file_serializer.validated_data['file']) in LEGAL_FORMATS:
                instance = file_serializer.save()
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s)
                # to do check response Content-Type
                # resp.set_headers({'Content-Type': 'multipart/form-data'})
                # resp['Content-Type'] = 'multipart/form-data'

                return resp
            else:
                return Response(file_serializer.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)

# image to PIL object
# instance = file_serializer.save()
# a=ImageClass.objects.get(file=instance.file)
# im=Image.open(a.file.path)
# im.show()
