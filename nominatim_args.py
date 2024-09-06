from argparse import Namespace
from pathlib import Path
from typing import Optional


class NominatimArgs(Namespace):
    """
    :py:class:`Namespace` Wrapper for a :py:class:`NominatimAPI` :py:class:`argparse.ArgumentParser`.

    :ivar input: Path to input :py:class:`locations.Locations` from.
    :ivar output: Path to output :py:class:`locations.Locations` to.
    :ivar lookup: Queries for the :py:func:`NominatimAPI.lookup` endpoint.
    :ivar search: Queries for the :py:func:`NominatimAPI.search` endpoint.
    :ivar string: Key Source (Mutex) - generate :py:attr:`key` from :py:class:`str`.
    :ivar file: Key Source (Mutex) - generate :py:attr:`key` from file in :py:class:`Path`.
    :ivar key: The :py:class:`cryptography.fernet.Fernet` key to use for en/decryption.
    """
    input: Path
    output: Path
    lookup: Optional[list[str]]
    search: Optional[list[str]]
    string: Optional[str] = None
    file: Optional[Path] = None
    key: Optional[bytes] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.string is not None:
            self.key = self.string.encode()
        elif self.file is not None:
            with open(self.file, "rb") as fp:
                self.key = fp.read()
        else:
            self.key = None
