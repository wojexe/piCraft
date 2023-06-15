```mermaid

classDiagram
    Operation ..> ImageClass
    ImageFacade ..> ImageClass
    Operation <|.. ResizeOperation
    Operation <|.. EnhanceOperation
    Operation <|.. CompressOperation
    Operation <|.. ChangeFormatOperation
    Operation <|.. ImageOperation
    ImageOperation o-- Operation
    ImageFacade *-- ImageOperation
    ImageFacade *-- PrepareGenerateResponse
    ImageFacade *-- ImageLoader
    ImageLoader ..> Model

    class Model{
        ImageField imageModel
    }

    class ImageClass{
        -ImageTypePIL image
        -String path
        +init()
        +setPath(String path)
        +getPath()
        +openImage()
        +closeImage()
        +getImage()
    }
    class ImageFacade{
        -ImageLoader imageLoad
        -ImageOperation imageOperations
        -PrepareGenerateResponse imagePrepareGenerateResponse

        +addOperation(Operation operation)
        +loadImage(String url,Imagetype img)
        +process(ImageClass img)
        +generateResponse(ImageClass img)
    }
    class PrepareGenerateResponse{
        +prepareForGenerateResponseImage(ImageClass img)$
    }
    class ImageOperation{
        Operation operations[]
        +addOperation(Operation operation)
        +process(ImageClass img)

    }
    class ImageLoader{
        +loadImageFromObject(Model Img,ImageClass img)$
        +loadImageFromPath(String path,ImageClass img)$

    }
    class Operation{
        +process(ImageClass img)*
    }
    <<abstract>> Operation
    class EnhanceOperation{
        +process(ImageClass img)
    }
    class CompressOperation{
        -int quality
        +process(ImageClass img)
    }
    class ResizeOperation{
        -int height
        -int width
        +process(ImageClass img)
    }
    class ChangeFormatOperation{
        -String format
        +process(ImageClass img)
    }


```