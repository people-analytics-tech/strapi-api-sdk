import requests


class Http:
    def __init__(self, api_base_url: str, timeout: int = 600):
        self.timeout = timeout
        self.api_base_url = api_base_url
        self.__headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if not self.api_base_url.endswith('/'):
            self.api_base_url = f"{self.api_base_url}/"

    def __http_request(
        self, 
        method: str, 
        endpoint: str, 
        headers: dict = {},
        data: dict = {}, 
        params: dict = {}
    ):
        url = f"{self.api_base_url}{endpoint}" 
        headers = {**self.__headers, **headers}
        timeout = self.timeout
        
        return requests.request(
            method=method,
            url=url,
            headers=headers,
            timeout=timeout,
            json=data,
            params=params,
        )

    def post(
        self, 
        endpoint: str, 
        headers: dict = {}, 
        data: dict = {}
    ):
        return self.__http_request(method="POST", endpoint=endpoint, headers=headers, data=data)

    def get(
        self, 
        endpoint: str, 
        headers: dict = {}, 
        data: dict = {}, 
        params: dict = {}
    ):
        return self.__http_request(
            method="GET", endpoint=endpoint, headers=headers, data=data, params=params
        )

    def put(
        self, 
        endpoint: str, 
        headers: dict = {}, 
        data: dict = {}
    ):
        return self.__http_request(method="PUT", endpoint=endpoint, headers=headers, data=data)

    def patch(
        self, 
        endpoint: str, 
        headers: dict = {}, 
        data: dict = {}
    ):
        return self.__http_request(method="PATCH", endpoint=endpoint, headers=headers, data=data)

    def delete(
        self, 
        endpoint: str, 
        headers: dict = {}, 
        data: dict = {}
    ):
        return self.__http_request(method="DELETE", endpoint=endpoint, headers=headers, data=data)
