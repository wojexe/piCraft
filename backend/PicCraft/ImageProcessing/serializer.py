from rest_framework import serializers
from . import models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ('id', 'file')


class ImageOperationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    height = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    rate = serializers.IntegerField(required=False)
    format = serializers.CharField(max_length=50, required=False)
