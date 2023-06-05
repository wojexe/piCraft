# πCraft

**πCraft** is a web application that provides the user with the ability to modify images. The modifications include operations like: resizing, compressing, enhancing and changing image format.

The application is composed of two parts: frontend and backend. The frontend empowers the user to interact with the REST API, made available by the backend server.

The backend processes images sent by the user and responds with the modified images. It does not store any data.

## Usage

TBD

### API Endpoints

Response schema for every endpoint:

```ts
{
    error?: {
        code: number;
        message?: string;
    };
    url?: string;
}
```

Request schema:

#### `/resize`

```ts
{
    image: base64;
    width: number;
    height: number;
}
```

#### `/compress`

```ts
{
    image: base64;
    compressionRate?: number;
}
```

#### `/enhance`

```ts
{
    image: base64;
}
```

#### `/change_format/[format]`

```ts
{
    image: base64;
    resultFormat: "png" | "jpeg" | "jpg" | "bmp" | "heic" | "gif"
                    | "gifv" | "webp" | "tiff";
}
```
