import argparse


class AppendKeyValueAction(argparse.Action):
    """Custom :py:class:`argparse.Action` "append" implementation that allows (key)-value pairs."""
    def __call__(self, parser, namespace, values, option_string=None):
        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            # Initialize the `self.dest` dictionary (Reminder: `Action.dest` defaults to action name/flag.)
            setattr(namespace, self.dest, {})
        dictionary = getattr(namespace, self.dest)
        match len(values):
            case 1:
                # --action "value"
                dictionary[values[0]] = values[0]
            case 2:
                # --action "key" "value"
                dictionary[values[0]] = values[1]
            case _:
                # default case
                raise argparse.ArgumentError(self, f"Expected 1 or 2 arguments, got {len(values)}")


def main():
    parser = argparse.ArgumentParser(description='Example with flexible key-value arguments')
    parser.add_argument("-v", "--value",
                        action=AppendKeyValueAction,
                        nargs='+',
                        help="Add a value to the dictionary. Use '-v value' or '--value key value'")
    args = parser.parse_args()
    print(args.value)


if __name__ == '__main__':
    main()
