# Strapi API SDK
Interact with Strapi functionalities within your python application, includes the ability to perform create, read, update, and delete (CRUD) operations on existing APIs endpoints and provides an Authenticator class ready to create new users, API Tokens and etc.

## Instalation
```sh
pip install strapi-api-sdk
```

# Configuration
## Environment variables
To use strapi-api-sdk, you need to set two environment variables:
```dotenv
# ---DOTENV EXAMPLE---
STRAPI_API_TOKEN= # Your API Token
STRAPI_BASE_URL=strapi.mybaseurl.com.br
```
You can later on change these two env variables if you want to.

_For the token change, use **StrapiAuthenticator().set_token()**_

_For the base URL change, call the http object on the desired client and use **http.set_api_base_url()**_

# Usage Example
You can use strapi-api-sdk to:
- Create, update and delete registers on all APIs that your Strapi application provides.
- Create a user inside Strapi with a specific or generic role (public, authenticated, etc).
- Create an API Token to a specific user (using the JWT auth from Strapi's core).

## Code example
```python
from strapi_api_sdk.sdk import (
    StrapiUser, 
    StrapiClient, 
    StrapiAuthenticator
)

# Instantiate clients.
auth = StrapiAuthenticator()
user = StrapiUser(auth=auth)
client = StrapiClient(auth=auth)

# Create a new user
# NOTE: In the absence of password parameter, the class creates a random URL-safe text string, in Base64 encoding and use it as the user password.
new_user = user.register_user(
    username="creation-tester2",
    email="creation2@tester.com.br",
    role_type="authenticated",
)

# Create an API token for this user
new_user_token = auth.create_token(
    identifier=new_user["username"], 
    password=new_user["password"]
)

# Retrieve some data.
api_data = client.get_entries(plural_api_id="some-apis", batch_size=100)
one_api_data = client.get_entry(plural_api_id="some-apis", document_id=1, populate=["*"])

# Create entry.
api_data_to_create_dict = {
    "foo": "bar",
    "num": 35
}
create_api_data = client.create_entry(plural_api_id="some-apis", data=api_data_to_create_dict)
```