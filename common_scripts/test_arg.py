import argparse
import sys

def showtop20():
    print('running showtop20')

def listapps():
    print('running listapps')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Create a showtop20 subcommand    
parser_showtop20 = subparsers.add_parser('showtop20', help='list top 20 by app')
parser_showtop20.set_defaults(func=showtop20)

# Create a listapps subcommand       
parser_listapps = subparsers.add_parser('listapps', help='list all available apps')
parser_listapps.set_defaults(func=listapps)

# Print usage message if no args are supplied.

# NOTE: Python 2 will error 'too few arguments' if no subcommand is supplied.
#       No such error occurs in Python 3, which makes it feasible to check
#       whether a subcommand was provided (displaying a help message if not).
#       argparse internals vary significantly over the major versions, so it's
#       much easier to just override the args passed to it.

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()

# Run the appropriate function (in this case showtop20 or listapps)
options.func()

# If you add command-line options, consider passing them to the function,
# e.g. `options.func(options)`
