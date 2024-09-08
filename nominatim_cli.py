from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Sequence

from append_key_value_action import AppendKeyValueAction
from nominatim_args import NominatimArgs


class NominatimCLI:
    """
    Command Line Interface for Nominatim.

    :ivar instance: Singleton Instance of the class.
    :ivar parser: Command-Line Argument Parser; Call :py:func:`parse_args` with `args=["--help"]` for details.
    """
    instance: 'NominatimCLI'
    parser: ArgumentParser

    def __new__(cls, *args, **kwargs):
        """Force Singleton (create :py:attr:`instance` if None, else return it)."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(NominatimCLI, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """:py:class:`NominatimCLI` Constructor."""
        parser = ArgumentParser()
        parser.add_argument("-i", "--input", type=Path, help="Path to import locations from.")
        parser.add_argument("-o", "--output", type=Path, help="Path to export locations to.")
        parser.add_argument("-s", "--search", action=AppendKeyValueAction, nargs='*',
                            help="Search queries; Surround with quotes for spaces, may prefix with key.")
        parser.add_argument("-l", "--lookup", action=AppendKeyValueAction, nargs='*',
                            help="Lookup OSM IDs; Surround with quotes for spaces, may prefix with key.")
        key_group = parser.add_mutually_exclusive_group()
        key_group.add_argument("-k", "--key", dest="string", help="Key string to use for en/decryption.")
        key_group.add_argument("-f", "--file", help="Path to key-file to use for en/decryption.")
        self.parser = parser

    def parse_args(self, args: Sequence[str] | None = None, namespace: Namespace | None = None):
        """Wrapper for :py:func:`ArgumentParser.parse_args` as :py:class:`NominatimArgs`."""
        return NominatimArgs(**self.parser.parse_args(args, namespace).__dict__)


def main():
    print(NominatimCLI().parse_args())


if __name__ == "__main__":
    main()
