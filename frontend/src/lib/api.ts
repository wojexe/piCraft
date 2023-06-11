export namespace PiCraftAPI {
  export const acceptedFileTypes = [
    ".png", ".jpeg", ".jpg", ".bmp", ".heic",
    ".gif", ".gifv", ".webp", ".tiff"
  ]

  export const availableModifications: Array<Modification> = [
    {
      name: "resize",
      display: "Resize",
      params: [
        {
          name: "width",
          display: "Width",
          type: "number"
        },
        {
          name: "height",
          display: "Height",
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
          display: "Compression rate",
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
          display: "Result format",
          type: "text"
        }
      ],
      endpoint: "/change_format"
    }
  ]

  export type Modification = {
    name: string,
    display: string,
    params: Array<ModificationParam>,
    endpoint: string
  }

  export type ModificationParam = {
    name: string,
    display: string,
    type: string
  }

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
