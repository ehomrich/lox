from sys import argv

from lox.lox import Lox


def main(args) -> None:
    if len(args) > 1:
        Lox.usage(64)
    elif len(args) == 1:
        Lox.run_file(args[0])
    else:
        Lox.prompt()


main(argv[1:])
