#!/usr/bin/env python3
import argparse
from ..base.pre_build_app import PreBuild


def main():

    _docker = False
    my_parser = argparse.ArgumentParser(
        prog='skeleton', description='List the content of a folder')

    # Add the arguments
    my_parser.add_argument('-f',
                           metavar='Framework',
                           type=str,
                           help='Seleccione Framework [falcon, fastapi ,flask]',
                           nargs=1,
                           choices=['falcon', 'fastapi'],
                           required=True),
    my_parser.add_argument('-n',
                           metavar='name',
                           type=str,
                           help='nombre del proyecto',
                           nargs=1,
                           required=True),

    my_parser.add_argument('-db',
                           metavar='DB',
                           type=str,
                           help='Seleccione DB [mongo]',
                           nargs=1,
                           choices=['mongo']),

    # my_parser.add_argument('-d',
    #                        metavar='Docker',
    #                        type=str,
    #                        help='Yes - No',
    #                        nargs=1,
    #                        choices=['Yes', 'no'])

    # Execute the parse_args() method
    args = my_parser.parse_args()
    _framework = "".join(args.f)
    _library = None

    _name_app = "".join(args.n)

    if 'db' in args:
        _db = "".join(args.db)

    # if 'd' in args and args.d == ['Yes']:
    #     _docker = True
    # _library = None

    #  execute skeleton
    _build = PreBuild(framework=_framework, db=_db,
                      name_app=_name_app, docker=_docker,
                      library=_library)
    _build.main()


if __name__ == "__main__":
    main()
