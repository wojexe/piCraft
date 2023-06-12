export const acceptedFileTypes = ["png", "jpeg", "jpg", "bmp", "heic", "gif", "gifv", "webp", "tiff"] as const;
export type AcceptedFileTypes = typeof acceptedFileTypes[number];

export const availableModifications = [
  {
    id: "resize",
    display: "Resize",
    endpoint: "/resize"
  },
  {
    id: "compress",
    display: "Compress",
    endpoint: "/compress"
  },
  {
    id: "enhance",
    display: "Enhance",
    endpoint: "/enhance"
  },
  {
    id: "changeFormat",
    display: "Change format",
    endpoint: "/change_format"
  }
] as const;

export type AvailableModifications = typeof availableModifications[number]["id"];

export const modificationParams: Record<AvailableModifications, Array<AnyParam>> = {
  resize: [
    {
      type: "number", id: "width", display: "Width",
      defaultValue: 256, min: 8, max: 8196
    },
    {
      type: "number", id: "height", display: "Height",
      defaultValue: 256, min: 8, max: 8196
    }
  ],
  compress: [
    {
      type: "number", id: "rate", display: "Compression rate",
      defaultValue: 80, min: 10, max: 100
    }
  ],
  enhance: [],
  changeFormat: [
    {
      type: "select", id: "format", display: "Result format",
      defaultValue: "jpg", selections: acceptedFileTypes
    }
  ]
};

export type Modification = {
  id: string;
  display: string;
  params: Array<AnyParam>;
  endpoint: string;
};

export interface ModificationParam {
  id: string;
  display: string;
  type: string;
}

export interface NumberParam extends ModificationParam {
  defaultValue: number;
  value?: number;
  min: number;
  max: number;
}

export interface SelectParam extends ModificationParam {
  defaultValue: any;
  value?: any;
  selections?: Array<any> | ReadonlyArray<any>;
}

export type AnyParam = NumberParam | SelectParam;

