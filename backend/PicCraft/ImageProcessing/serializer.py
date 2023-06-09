from rest_framework import serializers
from . import models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ('id', 'file')
