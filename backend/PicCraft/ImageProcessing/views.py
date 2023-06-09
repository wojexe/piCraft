from PIL import Image
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PhotoSerializer
from .models import Image as ImageClass
import imghdr
from django.http import FileResponse

# Create your views here.
LEGAL_FORMATS = ['jpg', 'jpeg', 'png','gifv', 'heic','gif', 'tiff', 'bmp', 'webp']
class Resize(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, *args, **kwargs):
        try:
            # todo: more validation data?
            # todo: logic for resizing
            file_serializer = PhotoSerializer(data=request.data)
            name = request.data['name']
            width = request.data['width']
            height = request.data['height']
            if file_serializer.is_valid() and name == 'resize' and int(width) > 0 and int(height) > 0 and imghdr.what(file_serializer.validated_data['file']) in LEGAL_FORMATS:
                instance=file_serializer.save()
                s=open(instance.file.path, 'rb')
                resp=FileResponse(s)
                #to do check response Content-Type
                # resp.set_headers({'Content-Type': 'multipart/form-data'})
                # resp['Content-Type'] = 'multipart/form-data'

                return resp
            else:
                return Response(file_serializer.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)


class Compress(APIView):
    def post(self, request):
        return render(request, 'index.html')


class Enhance(APIView):

    def post(self, request):
        return render(request, 'index.html')


class ChangeFormat(APIView):
    def post(self, request):
        return render(request, 'index.html')


class Combine(APIView):
    def post(self, request):
        return render(request, 'index.html')
