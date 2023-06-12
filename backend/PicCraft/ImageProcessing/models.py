from django.db import models
from django.core.validators import FileExtensionValidator

LEGAL_FORMATS = ['jpg', 'jpeg', 'png', 'gifv', 'heic', 'gif', 'tiff', 'bmp', 'webp']


class Image(models.Model):
    file = models.ImageField(validators=[FileExtensionValidator(allowed_extensions=LEGAL_FORMATS)])
