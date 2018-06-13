"""
================================================
                   i18nki v0.1
      Internationalization Key Interpreter
  (an easy to use localization file generator)
================================================

"""

import os
import time
import argparse

from i18nki.parser import Parser
from colorama import init, Fore, Back
from i18nki.compilers import ini, gettext, yaml

# initialize colorama
init(autoreset=True)

print('%s%s' % (Fore.CYAN, __doc__))

home = os.getcwd()
start = int(round(time.time() * 1000))


# get arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input', help='input directory', required=True)
argparser.add_argument('-o', '--output', help='output file', required=True)

argparser.add_argument(
    '-f', '--filter', help='regex filter to match source key (ie "load\((.*?)\)"', required=True)

argparser.add_argument(
    '-c', '--comment', help='comment string in source (ie "#" for python)', required=True)

argparser.add_argument(
    '--compiler', help='which compiler to use (ie INI, Gettext...) [default=INI]')

argparser.add_argument(
    '--separator', help='change default sepator character (ie ":" instead of "=" with ini)')

# parse arguments
args = argparser.parse_args()


# run parser
print('%sParser' % Back.CYAN)

try:
    os.chdir(args.input)
except (FileNotFoundError, NotADirectoryError):
    print('%sERR: %s is not a directory!' % (Fore.RED, args.input))
    exit(-1)

parser = Parser(args.filter, args.comment)
tree = parser.parse()
print()


# run compiler
print('%sCompiler' % Back.CYAN)
os.chdir(home)

# default compiler to INI
compiler_choice = args.compiler.lower() if args.compiler is not None else 'INI'
compiler = ini.INI(args.separator)

# change compiler option
if compiler_choice == 'gettext' or compiler_choice == 'po':
    compiler = gettext.Gettext()
elif compiler_choice == 'yaml' or compiler_choice == 'yml':
    compiler = yaml.YAML()

# compile tree
compiler.compile(tree, args.output)
print()


# done
print('%sProcess completed in %ims' %
      (Back.CYAN, int(round(time.time() * 1000)) - start))
