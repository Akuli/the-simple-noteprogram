#!/usr/bin/env python3
"""This file installs The Simple Noteprogram on Unix-like operating
systems such as GNU/Linux."""


import argparse
import sys


class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, default_args=None):
        argparse.ArgumentParser.__init__(self)
        if default_args is not None:
            for arg, kwargs in default_args.items():
                self.add_argument(arg, **kwargs)

    def error(self, *ign):
        self.print_help()
        sys.exit(1)


parser = ArgumentParser({
    'action':   dict(help="install or uninstall"),
    '--prefix': dict(help="use FOO to do foo things"),
})
args = parser.parse_args()
if args.action not in ('install', 'uninstall'):
    parser.error()

print("*" * 50)
print("Args are:", args)
