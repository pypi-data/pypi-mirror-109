import sys


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    # inicia la terminal para la creacion de proyectos
    from .cli.commands import main
    main()


if __name__ == "__main__":
    sys.exit(main())

