export namespace PiCraftAPI {
  export const acceptedFileTypes = [
    ".png", ".jpeg", ".jpg", ".bmp", ".heic",
    ".gif", ".gifv", ".webp", ".tiff"
  ]

  export const availableModifications = [
    {
      name: "resize",
      display: "Resize",
      params: [
        {
          name: "width",
          type: "number"
        },
        {
          name: "height",
          type: "number"
        }
      ],
      endpoint: "/resize"
    },
    {
      name: "compress",
      display: "Compress",
      params: [
        {
          name: "rate",
          type: "number"
        }
      ],
      endpoint: "/compress"
    },
    {
      name: "enhance",
      display: "Enhance",
      params: [],
      endpoint: "/enhance"
    },
    {
      name: "changeFormat",
      display: "Change format",
      params: [
        {
          name: "resultFormat",
          type: acceptedFileTypes
        }
      ],
      endpoint: "/change_format"
    }
  ]

  export type Resize = {
    Request: {

    },
    Response: {

    }
  }

  export type Compress = {
    Request: {

    },
    Response: {

    }
  }

  export type Enhance = {
    Request: {

    },
    Response: {

    }
  }
  export type changeFormat = {
    Request: {

    },
    Response: {

    }
  }
}
