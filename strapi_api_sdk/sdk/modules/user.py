# Ref: https://docs.strapi.io/dev-docs/plugins/users-permissions

import secrets

from requests import Response

from strapi_api_sdk.utils.constants import API_ENDPOINT_USERS_ROLES, API_ENDPOINT_USERS

from strapi_api_sdk.models.exceptions import UserError

from strapi_api_sdk.sdk.modules.http import Http
from strapi_api_sdk.sdk.modules.auth import StrapiAuthenticator


class StrapiUser:
    """Default client for Strapi user endpoints."""
    
    http: Http = None
    __auth_obj: StrapiAuthenticator = None

    def __init__(
        self,
        base_url: str,
        auth: StrapiAuthenticator,
        request_timeout: int = 600
    ) -> None:
        self.http: Http = Http(api_base_url=base_url, timeout=request_timeout)
        self.__auth_obj: StrapiAuthenticator = auth
    
    def __response_handler(self, response: Response) -> Response:
        if 200 <= response.status_code < 300:
            return response
        else:
            raise UserError(f'ERROR: {response.status_code}: {response.reason}')
          
    def __get_role_type_id(self, role_type: str) -> int:
        header = self.__auth_obj.get_auth_header()
        
        roles_data = self.__response_handler(
            self.http.get(endpoint=API_ENDPOINT_USERS_ROLES, headers=header)
        )
        
        roles_dict = roles_data.json()["roles"]
        role_id = list(filter(lambda dct: dct["type"] == role_type.lower(), roles_dict))
                
        if not role_id:
            raise UserError("The given role type to create user doesn't exists.")

        return int(role_id[0]["id"])
  
    def __register_user(
        self,
        username: str,
        email: str,
        password: str,
        role_type: str = "public"
    ) -> dict:
        header = self.__auth_obj.get_auth_header()
        body = {
            'username': username, 
            'email': email,
            'password': password,
            'role': self.__get_role_type_id(role_type=role_type)
        }
        
        user_register = self.__response_handler(
            self.http.post(endpoint=API_ENDPOINT_USERS, headers=header, data=body)
        )
        user_register_data = user_register.json()
        
        return {**user_register_data, "password": password}
    
    def register_user(
        self,
        username: str,
        email: str,
        password: str = None,
        role_type: str = "public"
    ) -> dict:
        """Register a new user to the selected role if the role exists."""
        if not password:
            password = secrets.token_urlsafe(32)
        
        register_data = self.__register_user(
            username=username,
            email=email,
            password=password,
            role_type=role_type
        )
        
        return register_data
