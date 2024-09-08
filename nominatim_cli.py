import os.path
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Sequence

from append_key_value_action import AppendKeyValueAction
from crypter import Crypter
from locations import Locations
from nominatim_api import NominatimAPI
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
        # TODO: Singleton? Static? Something else?
        if not hasattr(cls, 'instance'):
            cls.instance = super(NominatimCLI, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """:py:class:`NominatimCLI` Constructor."""
        parser = ArgumentParser(description="A simple CLI to query the Nominatim API and en/decode the results.")
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

    def run(self, args: Sequence[str] | None = None, namespace: Namespace | None = None):
        # TODO: Compartmentalize.
        parsed_args = self.parse_args(args, namespace)
        if parsed_args.key is not None:
            crypter = Crypter(parsed_args.key)
        else:
            crypter = Crypter()
        if parsed_args.input is not None and os.path.exists(parsed_args.input):
            input_locations = NominatimAPI.decode(crypter.decrypt_from_file(parsed_args.input))
        else:
            input_locations = Locations()
        if parsed_args.search is not None:
            search_locations = Locations({key: NominatimAPI.search(parsed_args.search[key]) for key in parsed_args.search})
        else:
            search_locations = Locations()
        if parsed_args.lookup is not None:
            lookup_locations = Locations({key: NominatimAPI.lookup(parsed_args.lookup[key]) for key in parsed_args.lookup})
        else:
            lookup_locations = Locations()
        combined_locations = input_locations + search_locations + lookup_locations
        if parsed_args.output is not None:
            crypter.encrypt_to_file(combined_locations.__bytes__(), parsed_args.output)
        return combined_locations


def main():
    # TODO: REPL
    result = NominatimCLI().run()
    print(result)


if __name__ == "__main__":
    main()
