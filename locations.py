import json
from dataclasses import dataclass
from typing import Optional

from location import Location


@dataclass
class Locations:
    """
    Manages a collection of :class:`Location` instances.

    :ivar locations: The underlying collection of :class:`Location` instances, indexed by :class:`str` key (name / UID).
    """
    locations: dict[str, Location]

    def __init__(self, locations: Optional[dict[str, Location]] = None):
        self.locations = locations if locations is not None else dict()

    def add(self, value: Location, key: Optional[str] = None):
        """
        Add a :class:`Location` to the :class:`Locations` instance; Key will default to its UID if not given.

        :param value: :class:`Location` to add.
        :param key: Key to index the :class:`Location` with; Defaults to its UID if not given.
        :return: None
        """
        key = key if key is not None else value.uid
        self.locations[key] = value

    @property
    def deflated(self):
        """Deflated :py:class:`dict[str, str]` of :py:attr:`locations`; Maps key to :py:attr:`Location.uid`."""
        return {key: self.locations[key].uid for key in self.locations}

    @property
    def serialized(self):
        """:py:module:`JSON` string of :py:attr:`deflated` :py:attr:`locations`; Maps key to :py:attr:`Location.uid`."""
        return json.dumps(self.deflated)

    def __bytes__(self):
        """The (:py:attr:`deflated`) :py:attr:`serialized` string representation of self, encoded as :class:`bytes`."""
        return self.serialized.encode()

    def __add__(self, other: 'Locations'):
        """
        # TODO: Document.

        :param other:
        :return:
        """
        combined = self.locations.copy()
        combined.update(other.locations)
        return Locations(combined)
