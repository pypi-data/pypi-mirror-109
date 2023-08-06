"""
An entry point for the PyFBA command
"""

import os
import sys
import argparse
import PyFBA
from .gapfill_from_roles import gapfill_from_roles

def full_help():
    """
    Just return the help text
    :return: The help
    """

    return f"""
Welcome to PyFBA version {PyFBA.__version__}

Please use one of these commands with their appropriate flags. Use pyfba <command> -h for more help

gapfill_roles\tGapfill Flux Balance Analysis from a list of functional roles
fluxes\tGiven a set of reactions that form a model, report the fluxes through those reactions

help\tThis help menu
version\tPrint the version and exit

    """


def run():
    """
    Run the appropriate pyfba command
    """


    if sys.argv[1] == 'help' or sys.argv[1] == '-h' or sys.argv[1] == '--help': 
        print(full_help())
        sys.exit(0)
    if sys.argv[1] == 'version' or sys.argv[1] == '-v' or sys.argv[1] == '--version':
        print(PyFBA.__version__)
        sys.exit(0)
    elif sys.argv[1] == 'gapfill_roles':
        gapfill_from_roles()
    elif sys.argv[1] == 'fluxes':
        sys.stderr.write("Sorry, not implemented yet.")
    else:
        sys.stderr.write(f"Sorry. Don't understand {args.command}.")
        sys.stderr.write(full_help())
        sys.exit(0)

