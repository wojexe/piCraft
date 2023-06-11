
from abc import ABC, abstractmethod
from PIL import Image
from io import BytesIO
import base64
from django.db import models
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import FileResponse

from .models import Image as Img


class ImageClass:
    """Image class for holding image Pillow object"""

    def __init__(self):
        self.image = None

    """Open image from path by PILLOW library, and save it to image member"""

    def setImage(self, path: str) -> None:
        self.image = Image.open(path)

    """Get image"""

    def getImage(self, path: str) -> Image:
        return self.image


class ImageLoad:
    """Image load class for loading image from path or object"""

    """Load image from object model"""

    @staticmethod
    def loadImageFromObject(model: Img, img: ImageClass) -> None:
        img.setImage(model.file.path)

    """Load image from path"""

    @staticmethod
    def loadImageFromPath(path: str, img: ImageClass) -> None:
        img.setImage(path)


class GenerateResponse:
    """Generate response class for generating response from image"""

    """Generate response from image, we are saving our changes to model file, and then we are returning it as response"""

    @staticmethod
    def generateResponseFromImage(img: ImageClass, model: Img) -> FileResponse:
        img.image.save(model.file.path)
        s = open(model.file.path, 'rb')
        response = FileResponse(s)
        return response


class Operation(ABC):
    """Abstract class for operations on image"""
    @abstractmethod
    def process(self, img: ImageClass):
        pass


class ImageOperation(Operation):
    """Composite class for operations on image"""
    def __init__(self):
        self.operations = []

    def add_operation(self, operation: Operation):
        self.operations.append(operation)

    def process(self, img: ImageClass):
        for operation in self.operations:
            operation.process(img)


class ResizeOperation(Operation):
    """Leaf of composite class for resizing image"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def process(self, img: ImageClass):
        pass

class EnhanceOperation(Operation):
    """Leaf of composite class for enhancing image"""
    def process(self, img: ImageClass):
        pass


class CompressOperation(Operation):
    """Leaf of composite class for compressing image"""
    def __init__(self, quality: int):
        self.quality = quality

    def process(self, img: ImageClass):
        pass

class ChangeFormatOperation(Operation):
    """Leaf of composite class for changing format of image"""
    def __init__(self, format: str):
        self.format = format

    def process(self, img: ImageClass):
        pass

class ImageFacade:
    """Facade class for image processing, we are using it to load image, process it and generate response"""
    def __init__(self):
        self.imageLoad = ImageLoad()
        self.imageOperations = ImageOperation()
        self.imageGenerateResponse = GenerateResponse()

    """Add operation to composite class"""
    def add_operation(self, operation: Operation):
        self.imageOperations.add_operation(operation)

    """Process image by composite class"""
    def process(self, img: ImageClass):
        self.imageOperations.process(img)
    """Generate response from image"""
    def generateResponse(self, img: ImageClass, model: Img):
        return self.imageGenerateResponse.generateResponseFromImage(img, model)

    """Load image from path"""
    def loadImage(self, model: Img, img: ImageClass):
        self.imageLoad.loadImageFromObject(model, img)

