# Ref: https://docs.strapi.io/dev-docs/plugins/users-permissions

import secrets

from typing import Optional
from requests import Response

from strapi_api_sdk.models.exceptions import AuthenticationError

from strapi_api_sdk.sdk.modules.http import Http


class Authenticator:
    """Default client for Strapi authentication endpoints."""
    
    __http: Http = None
    __base_url: str = ""
    __token: Optional[str] = None
    
    def __init__(self, base_url: str) -> None:
        self.__http: Http = Http()
        self.__base_url = base_url
        self.__token = None
    
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
        """Retrieve access token."""
        url = self.__base_url + 'api/auth/local'
        header = self.get_auth_header()
        body = {'identifier': identifier, 'password': password}
        
        user_auth_data = self.__response_handler(
            self.__http.post(url=url, headers=header, data=body)
        )

        user_auth_dict = user_auth_data.json()
        return user_auth_dict["jwt"]
          
    def __get_role_type_id(self, role_type: str) -> int:
        url = self.__base_url + "api/users-permissions/roles"
        header = self.get_auth_header()
        
        roles_data = self.__response_handler(
            self.__http.get(url=url, headers=header)
        )
        
        roles_dict = roles_data.json()["roles"]
        role_id = list(filter(lambda dct: dct["type"] == role_type.lower(), roles_dict))
                
        if not role_id:
            raise AuthenticationError("The given role type to create user doesn't exists.")

        return int(role_id[0]["id"])
  
    def __register_user(
        self,
        username: str,
        email: str,
        password: str,
        role_type: str = "public"
    ) -> dict:
        """Register a new user to the selected role if the role exists."""
        url = self.__base_url + 'api/users'
        header = self.get_auth_header()
        body = {
            'username': username, 
            'email': email,
            'password': password,
            'role': self.__get_role_type_id(role_type=role_type)
        }
        
        user_register = self.__response_handler(
            self.__http.post(url=url, headers=header, data=body)
        )

        user_register_data = user_register.json()
        return {**user_register_data, "password": password}

    def create_token(
        self,
        identifier: str,
        password: str,
        set_as_default_token: bool = False
    ) -> str:
        token = self.__create_auth(
            identifier=identifier,
            password=password
        )
        
        if set_as_default_token:
            self.__token = token

        return token
       
    def set_token(self, token: str) -> None:
        self.__token = token
          
    def get_auth_header(self) -> dict:
        if not self.__token:
            return {}
        
        if self.__token:
            return {"Authorization": f"Bearer {self.__token}"}
    
    def register_user(
        self,
        username: str,
        email: str,
        password: str = None,
        role_type: str = "public"
    ) -> dict:
        
        if not password:
            password = secrets.token_urlsafe(32)
        
        register_data = self.__register_user(
            username=username,
            email=email,
            password=password,
            role_type=role_type
        )
        
        return register_data