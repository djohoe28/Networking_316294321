from nominatim_cli import NominatimCLI


def main():
    NominatimCLI().parse_args(args=[
        '-s', 'Obama', "White House",
        '-s', "The Pope", 'Vatican',
        '-s', "Burgeranch HaKnesset",
        '-l', 'W228034523',
        '-k', "iQuZfgyy4kmEnJgWVKPTLk8uwHdi1lGaEvpdTeSQx6c=",
        '--output', 'locations.dat'])
    NominatimCLI().parse_args(args=[
        '--input', 'locations.dat',
        '-k', "iQuZfgyy4kmEnJgWVKPTLk8uwHdi1lGaEvpdTeSQx6c="
        '-l', 'Obama', 'W212978508',
    ])

if __name__ == "__main__":
    main()