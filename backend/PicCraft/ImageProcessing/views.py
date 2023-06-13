import json
from PIL import Image
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PhotoSerializer, ImageOperationSerializer
from .models import Image as ImageClass, LEGAL_FORMATS
import imghdr
from django.http import FileResponse
from . import utils as us
from pillow_heif import register_heif_opener
register_heif_opener()

MAX_LIMIT_RES = 8196
MIN_LIMIT_RES = 8
MAX_COMPRESS_RATE = 100
MIN_COMPRESS_RATE = 10

# Create your views here.


class Resize(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # todo: more validation data?
        # todo: logic for Resizing
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            operations = ImageOperationSerializer(data=request.POST)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer=operations.validated_data
            if operations_serializer['name'] != 'resize':
                return Response('Wrong name of request', status=400)
            try:
                width_image = int(operations_serializer['width'])
                height_image = int(operations_serializer['height'])
            except ValueError:
                return Response('Width and height must be integer', status=400)
            if width_image < MIN_LIMIT_RES or height_image < MIN_LIMIT_RES or width_image > MAX_LIMIT_RES or height_image > MAX_LIMIT_RES:
                return Response(f'Width and height must be beetwen {MIN_LIMIT_RES} and {MAX_LIMIT_RES}', status=400)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            # START LOGIC
            instance = file_serializer.save()

            # END LOGIC
            try:
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s, status=200)
            except:
                return Response('File not found', status=400)
            return resp
        except Exception as e:
            return Response(e, status=400)


# to do check response Content-Type
# resp.set_headers({'Content-Type': 'multipart/form-data'})
# resp['Content-Type'] = 'multipart/form-data'
class Compress(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            operations = ImageOperationSerializer(data=request.POST)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data

            if operations_serializer['name'] != 'compress':
                return Response('Wrong name of request', status=400)
            try:
                rate_image = int(operations_serializer['rate'])
            except ValueError:
                return Response('Rate of compression must be integer', status=400)
            if rate_image < MIN_COMPRESS_RATE or rate_image > MAX_COMPRESS_RATE:
                return Response(f'Compression rate must be beetwen {MIN_COMPRESS_RATE} and {MAX_COMPRESS_RATE}', status=400)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            # START LOGIC
            instance = file_serializer.save()

            # END LOGIC
            try:
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s, status=200)
            except:
                return Response('File not found', status=400)
            return resp
        except Exception as e:
            return Response(e, status=400)


class Enhance(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            operations = ImageOperationSerializer(data=request.POST)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data
            if operations_serializer['name'] != 'enhance':
                return Response('Wrong name of request', status=400)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            # START LOGIC
            instance = file_serializer.save()

            # END LOGIC
            try:
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s, status=200)
            except:
                return Response('File not found', status=400)
            return resp
        except Exception as e:
            return Response(e, status=400)


class ChangeFormat(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            operations = ImageOperationSerializer(data=request.POST)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data
            if operations_serializer['name'] != 'change_format':
                return Response('Wrong name of request', status=400)
            if operations_serializer['format'] not in LEGAL_FORMATS:
                return Response(f'Format must be in {LEGAL_FORMATS}', status=400)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            # START LOGIC
            instance = file_serializer.save()
            # END LOGIC
            try:
                s = open(instance.file.path, 'rb')
                resp = FileResponse(s, status=200)
            except:
                return Response('File not found', status=400)
            return resp
        except Exception as e:
            return Response(e, status=400)


class Combine(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            params_data = json.loads(request.POST['params'])
            operations = ImageOperationSerializer(data=params_data, many=True)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            instance = file_serializer.save()
            try:
                for obj in operations.validated_data:
                    name = obj.get('name')
                    if name == 'resize':
                        width = obj.get('width')
                        height = obj.get('height')
                        try:
                            width_image = int(width)
                            height_image = int(height)
                        except ValueError:
                            return Response('Width and height must be integer', status=400)
                        if width_image < MIN_LIMIT_RES or height_image < MIN_LIMIT_RES or width_image > MAX_LIMIT_RES or height_image > MAX_LIMIT_RES:
                            return Response(f'Width and height must be beetwen {MIN_LIMIT_RES} and {MAX_LIMIT_RES}', status=400)

                        # START LOGIC

                        # END LOGIC
                    elif name == 'compress':
                        rate = obj.get('rate')
                        try:
                            rate_image = int(rate)
                        except ValueError:
                            return Response('Rate of compression must be integer', status=400)
                        if rate_image < MIN_COMPRESS_RATE or rate_image > MAX_COMPRESS_RATE:
                            return Response(f'Compression rate must be beetwen {MIN_COMPRESS_RATE} and {MAX_COMPRESS_RATE}', status=400)

                        # START LOGIC

                        # END LOGIC

                    elif name == 'enhance':
                        pass
                        # START LOGIC

                        # END LOGIC

                    elif name == 'change_format':
                        format_image = obj.get('format')
                        if format_image not in LEGAL_FORMATS:
                            return Response(f'Format must be in {LEGAL_FORMATS}', status=400)
                        # START LOGIC

                        # END LOGIC

                    else:
                        return Response('Wrong name of request', status=400)



            except Exception as e:
                return Response(str(e), status=400)
            s = open(instance.file.path, 'rb')
            resp = FileResponse(s)

            return resp
        except Exception as e:
            return Response(str(e), status=400)
