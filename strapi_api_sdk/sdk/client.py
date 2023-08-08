from typing import Optional, List

from requests import Response

from strapi_api_sdk.sdk.modules.http import Http
from strapi_api_sdk.sdk.modules.auth import Authenticator

#from strapi_api_sdk.helpers.query_builder import QueryBuilder  # TODO

from strapi_api_sdk.utils.http_utils import stringify_parameters

from strapi_api_sdk.models.exceptions import ClientError


class Strapi:
    """Requests based REST API client for Strapi."""

    __http: Http = None
    __base_url: str = ""
    __auth_obj: Authenticator = None

    def __init__(self, base_url: str, auth: Authenticator) -> None:
        """Initialize client."""
        if not base_url.endswith('/'):
            base_url = base_url + '/'

        self.__http: Http = Http()
        self.__base_url = base_url
        self.__auth_obj = auth

    def __response_handler(self, response: Response) -> Response:
        if 200 <= response.status_code < 300:
            return response
        else:
            raise ClientError(f'ERROR: {response.status_code}: {response.reason}')

    def get_entry(
        self,
        plural_api_id: str,
        document_id: int,
        populate: Optional[List[str]] = None,
        fields: Optional[List[str]] = None
    ) -> dict:
        """Get entry by id."""
        populate_param = stringify_parameters('populate', populate)
        fields_param = stringify_parameters('fields', fields)
        
        params = {
            **populate_param,
            **fields_param
        }
        url = self.__base_url + f"api/{plural_api_id}/{document_id}"
        header = self.__auth_obj.get_auth_header()
    
        data = self.__response_handler(
            self.__http.get(
                url=url, 
                headers=header, 
                params=params
            )
        )
        
        return data.json()

    def get_entries(
        self,
        plural_api_id: str,
        sort: Optional[List[str]] = None,
        filters: Optional[dict] = None,
        populate: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        pagination: Optional[dict] = None,
        publication_state: Optional[str] = None,
        get_all: bool = False,
        batch_size: int = 100
    ) -> dict:
        """Get list of entries. Optionally can operate in batch mode to get all entries automatically."""
        sort_param = stringify_parameters('sort', sort)
        filters_param = stringify_parameters('filters', filters)
        populate_param = stringify_parameters('populate', populate)
        fields_param = stringify_parameters('fields', fields)
        pagination_param = stringify_parameters('pagination', pagination)
        publication_state_param = stringify_parameters('publicationState', publication_state)
        
        url = self.__base_url + f"api/{plural_api_id}"
            
        params = {
            **sort_param,
            **filters_param,
            **pagination_param,
            **populate_param,
            **fields_param,
            **publication_state_param
        }
        header = self.__auth_obj.get_auth_header()
        
        if not get_all:
            data = self.__response_handler(
                self.__http.get(
                    url=url, 
                    headers=header, 
                    params=params
                )
            )

            return data.json()
        
        if get_all:
            page = 1
            get_more = True

            while get_more:
                pagination = {
                    'page': page,
                    'pageSize': batch_size
                }
                pagination_param = stringify_parameters('pagination', pagination)
                
                for key in pagination_param:
                    params[key] = pagination_param[key]
                    
                res_obj1 = self.__response_handler(
                    self.__http.get(
                        url=url, 
                        headers=header,
                        params=params
                    )
                ).json()
                
                if page == 1:
                    res_obj = res_obj1
                else:
                    res_obj['data'] += res_obj1['data']
                    res_obj['meta'] = res_obj1['meta']
                    
                page += 1
                pages = res_obj['meta']['pagination']['pageCount']
                get_more = page <= pages
                
            return res_obj

    def create_entry(
        self,
        plural_api_id: str,
        data: dict
    ) -> dict:
        """Create entry."""
        url = self.__base_url + f"api/{plural_api_id}"
        header = self._get_auth_header()
        body = {
            'data': data
        }
        
        data = self.__response_handler(
            self.__http.post(
                url=url,  
                headers=header,
                data=body,
            )
        )
        
        return data.json()

    def update_entry(
        self,
        plural_api_id: str,
        document_id: int,
        data: dict
    ) -> dict:
        """Update entry fields."""
        url = self.__base_url + f"api/{plural_api_id}/{document_id}"
        header = self._get_auth_header()
        body = {
            'data': data
        }
        
        data = self.__response_handler(
            self.__http.put(
                url=url,  
                headers=header,
                data=body,
            )
        )
        
        return data.json()

    def delete_entry(
        self,
        plural_api_id: str,
        document_id: int
    ) -> dict:
        """Delete entry by id."""
        url = self.__base_url + f"api/{plural_api_id}/{document_id}"
        header = self._get_auth_header()
        
        data = self.__response_handler(
            self.__http.delete(
                url=url,  
                headers=header
            )
        )
        
        return data.json()

    def upsert_entry(
        self,
        plural_api_id: str,
        data: dict,
        keys: List[str],
        unique: bool = True
    ) -> dict:
        """Create entry or update fields."""
        filters = {}
        for key in keys:
            if data[key] is not None:
                filters[key] = {'$eq': data[key]}
            else:
                filters[key] = {'$null': 'true'}
                
        current_rec = self.get_entries(
            plural_api_id=plural_api_id,
            fields=['id'],
            sort=['id:desc'],
            filters=filters,
            pagination={'page': 1, 'pageSize': 1}
        )
        num = current_rec['meta']['pagination']['total']
        
        if unique and num > 1:
            raise ValueError(f'Keys are ambiguous, found {num} records')
        
        elif num >= 1:
            return self.update_entry(
                plural_api_id=plural_api_id,
                document_id=current_rec['data'][0]['id'],
                data=data
            )
            
        else:
            return self.create_entry(
                plural_api_id=plural_api_id,
                data=data
            )
