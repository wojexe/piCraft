import json
from PIL import Image
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PhotoSerializer
from .models import Image as ImageClass, LEGAL_FORMATS
import imghdr
from django.http import FileResponse
from . import utils as us
from pillow_heif import register_heif_opener

LIMIT = 10000

# Create your views here.
register_heif_opener()


class Resize(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # todo: more validation data?
        # todo: logic for Resizing
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            name = request.POST['name']
            width = request.POST['width']
            height = request.POST['height']

            if name != 'resize':
                return Response('Wrong name of request', status=400)
            try:
                width_image = int(width)
                height_image = int(height)
            except ValueError:
                return Response('Width and height must be integer', status=400)
            if width_image <= 0 or height_image <= 0 or width_image > LIMIT or height_image > LIMIT:
                return Response(f'Width and height must be positive and less than {LIMIT}', status=400)
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
            name = request.POST['name']
            rate = request.POST['rate']
            if name != 'compress':
                return Response('Wrong name of request', status=400)
            try:
                rate_image = int(rate)
            except ValueError:
                return Response('Rate of compression must be integer', status=400)
            if rate_image <= 0 or rate_image >= 100:
                return Response(f'Rate of compression must be positive and less than 100', status=400)
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
            name = request.POST['name']
            if name != 'enhance':
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
            name = request.POST['name']
            format_image = request.POST['format']
            if name != 'change_format':
                return Response('Wrong name of request', status=400)
            if format_image not in LEGAL_FORMATS:
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
            data=json.loads(request.POST["params"])
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            instance = file_serializer.save()
            try:
                for obj in data:
                    name = obj.get('name')
                    if name == 'resize':
                        width = obj.get('width')
                        height = obj.get('height')
                        try:
                            width_image = int(width)
                            height_image = int(height)
                        except ValueError:
                            return Response('Width and height must be integer', status=400)
                        if width_image <= 0 or height_image <= 0 or width_image > LIMIT or height_image > LIMIT:
                            return Response(f'Width and height must be positive and less than {LIMIT}', status=400)
                        # START LOGIC

                        # END LOGIC
                    elif name == 'compress':
                        rate = obj.get('rate')
                        try:
                            rate_image = int(rate)
                        except ValueError:
                            return Response('Rate of compression must be integer', status=400)
                        if rate_image <= 0 or rate_image >= 100:
                            return Response(f'Rate of compression must be positive and less than 100', status=400)
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
