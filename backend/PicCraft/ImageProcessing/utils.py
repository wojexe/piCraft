from abc import ABC, abstractmethod
from PIL import Image, ImageEnhance
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
        self.path = None

    """Open image from path by PILLOW library, and save it to image member"""

    def setPath(self, path: str) -> None:
        self.path = path

    def getPath(self) -> str:
        return self.path

    def openImage(self) -> None:
        self.image = Image.open(self.path)

    def closeImage(self) -> None:
        self.image.close()

    """Get image"""

    def getImage(self) -> Image:
        return self.image


class ImageLoader:
    """Image load class for loading image from path or object"""

    """Load image from object model"""

    @staticmethod
    def loadImageFromObject(model: Img, img: ImageClass) -> None:
        img.setPath(model.file.url)

    """Load image from path"""

    @staticmethod
    def loadImageFromPath(path: str, img: ImageClass) -> None:
        img.setPath(path)


class PrepareGenerateResponse:
    """Generate response class for generating response from image"""

    """Generate response from image, we are saving our changes to model file, and then we are returning it as response"""

    @staticmethod
    def prepareForGenerateResponseImage(img: ImageClass):
        img.openImage()
        img.image.save(img.getPath())
        img.closeImage()


class Operation(ABC):
    """Abstract class for operations on image"""

    @abstractmethod
    def process(self, img: ImageClass):
        pass


class ImageOperation(Operation):
    """Composite class for operations on image"""

    def __init__(self):
        self.operations = []

    def addOperation(self, operation: Operation):
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
        img.openImage()
        image = img.getImage()
        image = image.resize((self.width, self.height))
        image.save(img.getPath())
        img.closeImage()


class EnhanceOperation(Operation):
    """Leaf of composite class for enhancing image"""

    def process(self, img: ImageClass):
        img.openImage()
        image = img.getImage()
        image = image.convert("RGB")
        enhancer = ImageEnhance.Brightness(image)
        enhanced_image = enhancer.enhance(1.2)

        enhancer = ImageEnhance.Contrast(enhanced_image)
        enhanced_image = enhancer.enhance(1.2)

        enhancer = ImageEnhance.Sharpness(enhanced_image)
        enhanced_image = enhancer.enhance(1.5)

        enhanced_image.save(img.getPath())
        img.closeImage()

class CompressOperation(Operation):
    """Leaf of composite class for compressing image"""

    def __init__(self, quality: int):
        self.quality = quality

    def process(self, img: ImageClass):
        img.openImage()
        image = img.getImage()
        image.save(img.getPath(), quality=self.quality)
        img.closeImage()


class ChangeFormatOperation(Operation):
    """Leaf of composite class for changing format of image"""

    def __init__(self, format: str):
        self.format = format

    def process(self, img: ImageClass):
        url=img.getPath()
        dot_index = url.rfind('.')
        if dot_index != -1:
            new_url = url[:dot_index]
        else:
            new_url = url
        img.openImage()
        image = img.getImage()
        image.save(new_url + '.' + self.format)
        img.closeImage()
        img.setPath(new_url + '.' + self.format)



class ImageFacade:
    """Facade class for image processing, we are using it to load image, process it and generate response"""

    def __init__(self):
        self.imageLoad = ImageLoader()
        self.imageOperations = ImageOperation()
        self.imagePrepareGenerateResponse = PrepareGenerateResponse()

    """Add operation to composite class"""

    def addOperation(self, operation: Operation):
        self.imageOperations.addOperation(operation)

    """Process image by composite class"""

    def process(self, img: ImageClass):
        self.imageOperations.process(img)

    """Generate response from image"""

    def generateResponse(self, img: ImageClass):
        self.imagePrepareGenerateResponse.prepareForGenerateResponseImage(img)

    """Load image from path"""

    def loadImage(self, url: str, img: ImageClass):
        self.imageLoad.loadImageFromPath(url, img)
