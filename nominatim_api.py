import json
import logging
import time
from logging import getLogger
from typing import Literal
from urllib.parse import urljoin, parse_qsl

import requests

from location import Location
from locations import Locations


class NominatimAPI:
    """
    An interface for making requests to the Nominatim API.

    :var API_URL: The URL to use when sending a request to the API.
    :var API_PARAM_BY_ENDPOINT: The available endpoints and respective parameters for the API.
    :var API_PARAMS: Parameters to use when sending a request to the API.
    :var API_HEADERS: Headers to use when sending a request to the API.
    :var API_RATE: API rate limit in requests per second.
    """
    API_URL = "https://nominatim.openstreetmap.org"
    API_PARAM_BY_ENDPOINT = {
        "search": "q",
        "lookup": "osm_ids"
    }
    API_PARAMS = {
        "format": "jsonv2",
        "addressdetails": True,
        "limit": 1
    }
    API_HEADERS = {
        "User-Agent": "CollegeProject/1.0 (vegogetenksssj13@yahoo.com)"
    }
    API_RATE = 1
    LOGGER = getLogger(__name__)

    @classmethod
    def limit(cls):
        """Sleeps to :py:attr:`API_RATE` seconds to limit API call rate."""
        cls.LOGGER.debug(f"Sleeping {cls.API_RATE} seconds to limit API call rate...")
        time.sleep(cls.API_RATE)

    @classmethod
    def request(cls, endpoint: Literal["search", "lookup"], parameter: str):
        """
        Makes the specified request to the API.

        :param endpoint: Which endpoint to use? ("search" or "lookup")
        :param parameter: Query for the endpoint; May contain additional parameters (e.g: "<value1>&<param2>=<value2>")
        :return: The first matching :py:class:`Location` received from Nominatim.
        """
        print(f"{endpoint.upper()}: {parameter}...")
        cls.limit()
        parsed = dict(parse_qsl(f"{cls.API_PARAM_BY_ENDPOINT[endpoint]}={parameter}"))  # Parse parameter(s) to dict.
        params = {**cls.API_PARAMS, **parsed}  # Combine default params with parsed parameter(s).
        return requests.get(urljoin(cls.API_URL, endpoint), params=params, headers=cls.API_HEADERS)

    @classmethod
    def search(cls, query: str):
        """
        Returns the first matching :class:`Location` for SEARCH with the given :param:`query`.

        :param query: Query describing the desired location.
        :return: The first match from Nominatim.
        """
        cls.LOGGER.debug(f"NominatimAPI.search({query})")
        response = cls.request("search", query)
        cls.LOGGER.info(f"search(query={query}) = {response}")
        return Location(**response.json()[0])

    @classmethod
    def lookup(cls, osm_id: str):
        """
        Returns the first matching :class:`Location` for LOOKUP with the given :param:`osm_id`.

        :param osm_id: Desired OpenStreetMap ID.
        :return: The first match from Nominatim.
        """
        cls.LOGGER.debug(f"NominatimAPI.lookup({osm_id})")
        response = cls.request("lookup", osm_id)
        cls.LOGGER.info(f"lookup(osm_ids={osm_id}) = {response}")
        return Location(**response.json()[0])

    @classmethod
    def inflate(cls, deflated: dict[str, str]):
        """
        Inflates a :py:attr:`Locations.deflated` collection by querying LOOKUP for the :py:attr:`Locations.uid`.

        :param deflated: The :py:attr:`Locations.deflated` collection to inflate.
        :return: Inflated :py:class:`Locations`.
        """
        return Locations({key: cls.lookup(deflated[key]) for key in deflated})

    @classmethod
    def deserialize(cls, serialized: str):
        """
        # TODO: Document.

        :param serialized:
        :return:
        """
        return cls.inflate(json.loads(serialized))

    @classmethod
    def decode(cls, encoded: bytes):
        """
        # TODO: Document.

        :param encoded:
        :return:
        """
        return cls.deserialize(encoded.decode())


def main():
    logging.basicConfig(level=logging.INFO)
    book = Locations({query: NominatimAPI.search(query) for query in ["Burgeranch HaKnesset", "Vatican City"]})
    book.add(NominatimAPI.lookup("W228034523"), "Tel Hai Parking Lot")
    print(NominatimAPI.inflate(book.deflated))


if __name__ == "__main__":
    main()
