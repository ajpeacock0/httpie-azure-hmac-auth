# httpie-azure-hmac-auth

[HMAC](https://tools.ietf.org/html/rfc2104) auth plugin for [HTTPie](https://httpie.org/) and [Azure Communuication Service](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/communication)

## Installation

> PiP lib coming soon...

## Usage

```bash
$ http --auth-type=azure-hmac --auth=':client-secret' https://<resource-name>.communication.azure.com/<endpoint>?api-version=<api-version>
```

Since the Azure Communuication Service (ACS) does not use a access key, yet the HTTPie `--auth` flag requires a "key:secret", a `:` is required to prefix the secret.

## ACS HMAC Scheme

HTTP requests will be signed with a shared secret key using HMAC. The string to sign format is:

| Header              | Description                                                                                                                                                                                           |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Host                | Internet host and port number.                                                                                                                                                                        |
| Date                | Date and time at which the request was originated. It can't be more than 15 minutes off from the current Coordinated Universal Time (Greenwich Mean Time). The value is an HTTP-date                  |
| x-ms-date           | Same as Date above. You can use it instead when the agent can't directly access the Date request header, or a proxy modifies it. If x-ms-date and Date are both provided, x-ms-date takes precedence. |
| x-ms-content-sha256 | base64 encoded SHA256 hash of the request body. It must be provided even if there is no body. base64_encode(SHA256(body))                                                                             |
| Authorization       | Authentication information required by the HMAC-SHA256 scheme. Format and details are explained later in this article.                                                                                |

```
METHOD + "\n"
URLPathAndQuery + "\n"
DateHeaderValue + ";" + HostHeaderValue + ";" + ContentHashHeaderValue
```

**Authorization Header Template**

```
Authorization: HMAC-SHA256 SignedHeaders=<value>&Signature=<value>
```

**Authorization Header Template**

```
Authorization: HMAC-SHA256 SignedHeaders=date;host;x-ms-content-sha256&Signature={}
```

| Argument      | Description                                             |
|---------------|---------------------------------------------------------|
| HMAC-SHA256   | Authorization scheme. (required)                        |
| SignedHeaders | HTTP request headers added to the signature. (required) |
| Signature     | base64 encoded HMACSHA256 of String-To-Sign. (required) |
