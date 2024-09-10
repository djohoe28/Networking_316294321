from argparse import Namespace
from pathlib import Path
from typing import Optional


class NominatimArgs(Namespace):
    """
    :py:class:`Namespace` Wrapper for a :py:class:`NominatimAPI` :py:class:`argparse.ArgumentParser`.

    :ivar imports: Path to input :py:class:`locations.Locations` from.
    :ivar exports: Path to output :py:class:`locations.Locations` to.
    :ivar lookup: Queries for the :py:func:`NominatimAPI.lookup` endpoint.
    :ivar search: Queries for the :py:func:`NominatimAPI.search` endpoint.
    :ivar string: Key Source (Mutex) - generate :py:attr:`key` from :py:class:`str`.
    :ivar file: Key Source (Mutex) - generate :py:attr:`key` from file in :py:class:`Path`.
    :ivar key: The :py:class:`cryptography.fernet.Fernet` key to use for en/decryption.
    """
    imports: Path
    exports: Path
    lookup: Optional[dict[str, str]]
    search: Optional[dict[str, str]]
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
