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
import os
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
            params_data = json.loads(request.POST['params'])
            operations = ImageOperationSerializer(data=params_data, many=False)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data
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
            try:
                instance = file_serializer.save()
                img = us.ImageClass()
                imgFacade = us.ImageFacade()
                imgFacade.loadImage(instance.file.path, img)
                imgFacade.addOperation(us.ResizeOperation(width_image, height_image))
                imgFacade.process(img)
                imgFacade.generateResponse(img)
                s = open(img.getPath(), 'rb')

                class DeleteFile(FileResponse):
                    def close(self):
                        super(DeleteFile, self).close()
                        instance.delete()

                response = DeleteFile(s)
                return response
            except Exception as e:
                return Response(e, status=400)

        except Exception as e:
            return Response(e, status=400)


class Compress(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            params_data = json.loads(request.POST['params'])
            operations = ImageOperationSerializer(data=params_data, many=False)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data
            try:
                rate_image = int(operations_serializer['rate'])
            except ValueError:
                return Response('Rate of compression must be integer', status=400)
            if rate_image < MIN_COMPRESS_RATE or rate_image > MAX_COMPRESS_RATE:
                return Response(f'Compression rate must be beetwen {MIN_COMPRESS_RATE} and {MAX_COMPRESS_RATE}', status=400)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            # START LOGIC
            try:
                instance = file_serializer.save()
                img = us.ImageClass()
                imgFacade = us.ImageFacade()
                imgFacade.loadImage(instance.file.path, img)
                imgFacade.addOperation(us.CompressOperation(rate_image))
                imgFacade.process(img)
                imgFacade.generateResponse(img)
                s = open(img.getPath(), 'rb')

                class DeleteFile(FileResponse):
                    def close(self):
                        super(DeleteFile, self).close()
                        instance.delete()

                response = DeleteFile(s)
                return response
            except Exception as e:
                return Response(e, status=400)

        except Exception as e:
            return Response(e, status=400)


class Enhance(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            params_data = json.loads(request.POST['params'])
            operations = ImageOperationSerializer(data=params_data, many=False)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            try:
                instance = file_serializer.save()
                img = us.ImageClass()
                imgFacade = us.ImageFacade()
                imgFacade.loadImage(instance.file.path, img)
                imgFacade.addOperation(us.EnhanceOperation())
                imgFacade.process(img)
                imgFacade.generateResponse(img)
                s = open(img.getPath(), 'rb')

                class DeleteFile(FileResponse):
                    def close(self):
                        super(DeleteFile, self).close()
                        instance.delete()

                response = DeleteFile(s)
                return response
            except Exception as e:
                return Response(e, status=400)
        except Exception as e:
            return Response(e, status=400)


class ChangeFormat(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            file_serializer = PhotoSerializer(data=request.FILES)
            params_data = json.loads(request.POST['params'])
            operations = ImageOperationSerializer(data=params_data, many=False)
            if not operations.is_valid():
                return Response(operations.errors, status=400)
            operations_serializer = operations.validated_data
            if operations_serializer['format'] not in LEGAL_FORMATS:
                return Response(f'Format must be in {LEGAL_FORMATS}', status=400)
            if not file_serializer.is_valid():
                return Response(file_serializer.errors.get("file")[0], status=400)
            try:
                instance = file_serializer.save()
                img = us.ImageClass()
                imgFacade = us.ImageFacade()
                imgFacade.loadImage(instance.file.path, img)
                imgFacade.addOperation(us.ChangeFormatOperation(
                    operations_serializer['format']))
                imgFacade.process(img)
                imgFacade.generateResponse(img)
                s = open(img.getPath(), 'rb')

                class DeleteFile(FileResponse):
                    def close(self):
                        super(DeleteFile, self).close()
                        instance.delete()
                        if os.path.isfile(img.getPath()):
                            os.remove(img.getPath())

                response = DeleteFile(s)
                return response
            except Exception as e:
                return Response(e, status=400)
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
            img = us.ImageClass()
            imgFacade = us.ImageFacade()
            imgFacade.loadImage(instance.file.path, img)

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
                        imgFacade.addOperation(
                            us.ResizeOperation(width_image, height_image))
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
                        imgFacade.addOperation(
                            us.CompressOperation(rate_image))
                        # END LOGIC

                    elif name == 'enhance':
                        # START LOGIC
                        imgFacade.addOperation(us.EnhanceOperation())
                        # END LOGIC

                    elif name == 'change_format':
                        format_image = obj.get('format')
                        if format_image not in LEGAL_FORMATS:
                            return Response(f'Format must be in {LEGAL_FORMATS}', status=400)
                        # START LOGIC
                        imgFacade.addOperation(
                            us.ChangeFormatOperation(format_image))
                        # END LOGIC

                    else:
                        return Response('Wrong name of request', status=400)

            except Exception as e:
                return Response(str(e), status=400)

            imgFacade.process(img)
            imgFacade.generateResponse(img)
            s = open(img.getPath(), 'rb')

            class DeleteFile(FileResponse):
                def close(self):
                    super(DeleteFile, self).close()
                    instance.delete()
                    if os.path.isfile(img.getPath()):
                        os.remove(img.getPath())

            response = DeleteFile(s)
            return response
        except Exception as e:
            return Response(str(e), status=400)
