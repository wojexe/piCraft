import { PUBLIC_PICRAFT_API } from "$env/static/public";

export const acceptedFileTypes = ["png", "jpeg", "jpg", "bmp", "heic", "gif", "webp", "tiff"] as const;
export type AcceptedFileTypes = typeof acceptedFileTypes[number];

export const availableModifications = [
  {
    id: "resize",
    display: "Resize",
    endpoint: "resize"
  },
  {
    id: "compress",
    display: "Compress",
    endpoint: "compress"
  },
  {
    id: "enhance",
    display: "Enhance",
    endpoint: "enhance"
  },
  {
    id: "changeFormat",
    display: "Change format",
    endpoint: "change_format"
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

type ModificationFetch = (file: File, modification: Array<Modification>) => Promise<Response>;

export const modificationFetch: ModificationFetch = (file: File, modifications: Array<Modification>) => {
  let endpoint;

  if (modifications.length === 1) {
    endpoint = modifications[0].endpoint;
  } else {
    endpoint = "combine"
  }

  const url = new URL(endpoint, PUBLIC_PICRAFT_API);

  const formData = new FormData();

  formData.append("file", file);

  // TODO: add more specific type
  type Param = { name: string } & { [key: string]: string };

  let body: Param | Array<Param>;
  if (modifications.length === 1) {
    const modification = modifications[0];

    body = {
      name: modification.endpoint,
      ...modification.params.reduce((obj, param) =>
        ({ ...obj, [param.id]: param.value ?? param.defaultValue }), {})
    }
  } else {
    body = modifications.map(modification => ({
      name: modification.endpoint,
      ...modification.params.reduce((obj, param) =>
        ({ ...obj, [param.id]: param.value ?? param.defaultValue }), {})
    }))
  }

  formData.append("params", JSON.stringify(body));

  return fetch(url, {
    method: "POST",
    body: formData
  });
}

export type Modification = {
  id: AvailableModifications;
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
  defaultValue: string;
  value?: string;
  selections?: Array<any> | ReadonlyArray<any>;
}

export type AnyParam = NumberParam | SelectParam;

