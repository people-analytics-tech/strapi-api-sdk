# Ref: https://docs.strapi.io/dev-docs/plugins/users-permissions

from requests import Response

from strapi_api_sdk.utils.constants import API_ENDPOINT_AUTH_LOCAL

from strapi_api_sdk.settings import API_TOKEN

from strapi_api_sdk.models.exceptions import AuthenticationError

from strapi_api_sdk.sdk.modules.http import Http


class StrapiAuthenticator:
    """Default client for Strapi authentication endpoints."""
    
    http: Http = None
    __token: str = None
    
    def __init__(
        self, 
        base_url: str,
        api_token: str,
        request_timeout: int = 600
    ) -> None:
        self.http: Http = Http(api_base_url=base_url, timeout=request_timeout)
        self.__token: str = api_token
    
    def __response_handler(self, response: Response) -> Response:
        if 200 <= response.status_code < 300:
            return response
        else:
            raise AuthenticationError(f'ERROR: {response.status_code}: {response.reason}')
    
    def __create_auth(
        self,
        identifier: str, 
        password: str
    ) -> str:
        header = self.get_auth_header()
        body = {'identifier': identifier, 'password': password}
        
        user_auth_data = self.__response_handler(
            self.http.post(endpoint=API_ENDPOINT_AUTH_LOCAL, headers=header, data=body)
        )

        user_auth_dict = user_auth_data.json()
        return user_auth_dict["jwt"]
          
    def create_token(
        self,
        identifier: str,
        password: str,
        set_as_current_token: bool = False
    ) -> str:
        """Retrieve access token."""
        token = self.__create_auth(
            identifier=identifier,
            password=password
        )
        
        if set_as_current_token:
            self.__token = token

        return token
       
    def set_token(self, token: str) -> None:
        """Set access token."""
        self.__token = token
          
    def get_auth_header(self) -> dict:
        """Retrieve Bearer token header for http requests."""
        if not self.__token:
            return {}
        
        if self.__token:
            return {"Authorization": f"Bearer {self.__token}"}
