from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal, Optional


@dataclass
class Location:
    """
    Represents a (parsed JSON) location obtained from the external API, Nominatim.

    :ivar place_id: The self's (non-persistent) ID on Nominatim's internal database.
    :ivar licence: The Nominatim license.
    :ivar osm_type: The self's type on OpenStreetMap ("node", "way", or "relation").
    :ivar osm_id: The self's ID on OpenStreetMap.
    :ivar lat: The latitude coordinate of the (centroid of the) self.
    :ivar lon: The longitude coordinate of the (centroid of the) self.
    :ivar category: The self's category (key) on OpenStreetMap's tag.
    :ivar type: The self's type (value) on OpenStreetMap's tag.
    :ivar place_rank: See:
        `Search Rank <https://nominatim.org/release-docs/latest/customize/Ranking/#search-rank>`_.
    :ivar importance: See:
        `Importance <https://nominatim.org/release-docs/latest/customize/Importance/#how-importance-is-computed>`_.
    :ivar addresstype: Address Type of self; :py:attr:`class` for "places", :py:attr:`type` for "regions".
    :ivar name: Localized name of the self.
    :ivar display_name: Full, comma-separated address of the self.
    :ivar address: Dictionary of address details for the self; Added with `addressdetails=1` parameter.
    :ivar boundingbox: Comma-separated list of corner coordinates for the self.
    """
    place_id: int
    licence: str
    osm_type: Literal["node", "way", "relation"]
    osm_id: int
    lat: Decimal
    lon: Decimal
    category: str
    type: str
    place_rank: int
    importance: float
    addresstype: str
    name: str
    display_name: str
    address: Optional[dict] = field(default_factory=dict)  # See NOTE below
    boundingbox: [Decimal, Decimal, Decimal, Decimal] = field(default_factory=list)  # See NOTE below

    # NOTE: the `= field(default_factory={class})` was suggested by ChatGPT,
    # since (apparently) `@dataclass` default values are re-used across fields.
    # i.e.: new `self` instances will be referencing the same `dict`/`list` instance(s) on initialization.

    def __post_init__(self):
        """Post-initialization; Turn fractional-value numeric strings into :class:`Decimal` instances."""
        self.lat = Decimal(self.lat)
        self.lon = Decimal(self.lon)
        for idx in range(len(self.boundingbox)):
            self.boundingbox[idx] = Decimal(self.boundingbox[idx])

    @property
    def uid(self) -> str:
        """
        An `attempted`_ unique identifier string of self.

        .. _attempted: https://nominatim.org/release-docs/latest/api/Output/#place_id-is-not-a-persistent-id
        """
        return f"{self.osm_type[0]}{self.osm_id}&{self.category}={self.type}"
