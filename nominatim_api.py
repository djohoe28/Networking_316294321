import time
from urllib.parse import urljoin

import requests

from location import Location


class NominatimAPI:
    """
    An interface for making requests to the Nominatim API.

    :var API_URL: The URL to use when sending a request to the API.
    :var API_ENDPOINT: The endpoint to use when sending a request to the API.
    :var API_PARAMETER_NAME: Parameter Name to use when sending a request to the API.
    :var API_PARAMS: Parameters to use when sending a request to the API.
    :var API_HEADERS: Headers to use when sending a request to the API.
    :var API_RATE: API rate limit in requests per second.
    """
    API_URL = "https://nominatim.openstreetmap.org"
    API_ENDPOINT = "search"
    API_PARAMETER_NAME = "q"
    API_PARAMS = {
        "format": "jsonv2",
        "addressdetails": True,
        "limit": 1
    }
    API_HEADERS = {
        "User-Agent": "CollegeProject/1.0 (vegogetenksssj13@yahoo.com)"
    }
    API_RATE = 1

    @classmethod
    def query_location(cls, query: str):
        """
        Returns the first matching :class:`Location` for the given :param:`query`.

        :param query: Query describing the desired location.
        :return: The first matching location received from Nominatim.
        """
        time.sleep(cls.API_RATE)
        response = requests.get(urljoin(cls.API_URL, cls.API_ENDPOINT),
                                params={**cls.API_PARAMS, cls.API_PARAMETER_NAME: query},
                                headers=cls.API_HEADERS)
        return Location(**response.json()[0])


if __name__ == "__main__":
    print(NominatimAPI.query_location("93 Rothschild Blvd Tel Aviv"))
