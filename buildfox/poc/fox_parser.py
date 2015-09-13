#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS


__version__ = (2015, 9, 13, 16, 59, 3, 6)

__all__ = [
    'fox_Parser',
    'fox_Semantics',
    'main'
]


class fox_Parser(Parser):
    def __init__(self, whitespace=re.compile(' +', RE_FLAGS | re.DOTALL), nameguard=None, **kwargs):
        super(fox_Parser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re='#.*?$',
            eol_comments_re='#.*?$',
            ignorecase=None,
            **kwargs
        )

    @graken()
    def _whitespace_opt_(self):
        self._pattern(r' *')

    @graken()
    def _eol_(self):
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

    @graken()
    def _simple_varname_(self):
        self._pattern(r'[a-zA-Z0-9_-]+')

    @graken()
    def _varname_(self):
        self._pattern(r'[a-zA-Z0-9_.-]+')

    @graken()
    def _EXPR_(self):
        self._pattern(r'(\$\n|.)*?$')

    @graken()
    def _PATH_(self):
        self._pattern(r'((?<!\$)\$\n|\$ |\$:|[^ :|\n])+')

    @graken()
    def _REGEX_OR_PATH_(self):
        self._pattern(r'r"(?![*+?])(?:[^\r\n\[\"/\\]|\\.|\[(?:[^\r\n\]\\]|\\.)*\])+"|((?<!\$)\$\n|\$ |\$:|[^ :|\n])+')

    @graken()
    def _path_once_(self):
        self._PATH_()

    @graken()
    def _paths_(self):

        def block0():
            self._PATH_()
            self.ast.setlist('@', self.last_node)
            self._pattern(r' *')
        self._closure(block0)

    @graken()
    def _assign_(self):
        self._varname_()
        self.ast['assign'] = self.last_node
        self._token('=')
        self._pattern(r' *')

        self._EXPR_()
        self.ast['value'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self.ast._define(
            ['assign', 'value'],
            []
        )

    @graken()
    def _assign_paths_(self):
        self._varname_()
        self.ast['assign'] = self.last_node
        self._token('=')
        self._pattern(r' *')

        self._paths_()
        self.ast['value'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self.ast._define(
            ['assign', 'value'],
            []
        )

    @graken()
    def _filter_var_(self):
        self._pattern(r' *')

        self._varname_()
        self.ast['var'] = self.last_node
        self._token(':')
        self._pattern(r' *')

        self._REGEX_OR_PATH_()
        self.ast['value'] = self.last_node

        self.ast._define(
            ['var', 'value'],
            []
        )

    @graken()
    def _FILTER_VARS_(self):

        def block0():
            self._filter_var_()
            self.ast.setlist('@', self.last_node)
        self._positive_closure(block0)

    @graken()
    def _SCOPED_VARS_(self):

        def block0():
            self._pattern(r'  ')
            self._assign_()
            self.ast.setlist('@', self.last_node)
        self._closure(block0)

    @graken()
    def _SCOPED_PATHS_(self):

        def block0():
            self._pattern(r'  ')
            self._assign_paths_()
            self.ast.setlist('@', self.last_node)
        self._closure(block0)

    @graken()
    def _rule_(self):
        self._token('rule')
        self._varname_()
        self.ast['rule'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self._SCOPED_VARS_()
        self.ast['vars'] = self.last_node

        self.ast._define(
            ['rule', 'vars'],
            []
        )

    @graken()
    def _build_(self):
        self._token('build')
        self._paths_()
        self.ast['targets_explicit'] = self.last_node
        with self._optional():
            self._pattern(r'(?<!\|)\|(?!\|)')
            self._paths_()
            self.ast['targets_implicit'] = self.last_node
        self._pattern(r':')
        self._varname_()
        self.ast['build'] = self.last_node
        self._paths_()
        self.ast['inputs_explicit'] = self.last_node
        with self._optional():
            self._pattern(r'(?<!\|)\|(?!\|)')
            self._paths_()
            self.ast['inputs_implicit'] = self.last_node
        with self._optional():
            self._pattern(r'\|\|')
            self._paths_()
            self.ast['inputs_order'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self._SCOPED_VARS_()
        self.ast['vars'] = self.last_node

        self.ast._define(
            ['targets_explicit', 'targets_implicit', 'build', 'inputs_explicit', 'inputs_implicit', 'inputs_order', 'vars'],
            []
        )

    @graken()
    def _default_(self):
        self._token('default')
        self._paths_()
        self.ast['defaults'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self.ast._define(
            ['defaults'],
            []
        )

    @graken()
    def _pool_(self):
        self._token('pool')
        self._varname_()
        self.ast['pool'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self._SCOPED_VARS_()
        self.ast['vars'] = self.last_node

        self.ast._define(
            ['pool', 'vars'],
            []
        )

    @graken()
    def _include_(self):
        self._token('include')
        self._path_once_()
        self.ast['include'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self.ast._define(
            ['include'],
            []
        )

    @graken()
    def _subninja_(self):
        self._token('subninja')
        self._path_once_()
        self.ast['subninja'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self.ast._define(
            ['subninja'],
            []
        )

    @graken()
    def _filter_(self):
        self._token('filter')
        self._FILTER_VARS_()
        self.ast['filters'] = self.last_node
        self._pattern(r' *')

        self._pattern(r'(\n|$)')

        self._SCOPED_VARS_()
        self.ast['vars'] = self.last_node

        self.ast._define(
            ['filters', 'vars'],
            []
        )

    @graken()
    def _manifest_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._rule_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._build_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._default_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._pool_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._include_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._subninja_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._assign_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._filter_()
                    self.ast.setlist('@', self.last_node)
                self._error('no available options')
        self._closure(block0)
        self._check_eof()


class fox_Semantics(object):
    def whitespace_opt(self, ast):
        return ast

    def eol(self, ast):
        return ast

    def simple_varname(self, ast):
        return ast

    def varname(self, ast):
        return ast

    def EXPR(self, ast):
        return ast

    def PATH(self, ast):
        return ast

    def REGEX_OR_PATH(self, ast):
        return ast

    def path_once(self, ast):
        return ast

    def paths(self, ast):
        return ast

    def assign(self, ast):
        return ast

    def assign_paths(self, ast):
        return ast

    def filter_var(self, ast):
        return ast

    def FILTER_VARS(self, ast):
        return ast

    def SCOPED_VARS(self, ast):
        return ast

    def SCOPED_PATHS(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def build(self, ast):
        return ast

    def default(self, ast):
        return ast

    def pool(self, ast):
        return ast

    def include(self, ast):
        return ast

    def subninja(self, ast):
        return ast

    def filter(self, ast):
        return ast

    def manifest(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = fox_Parser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in fox_Parser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for fox_.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-n', '--no-nameguard', action='store_true',
                        dest='no_nameguard',
                        help="disable the 'nameguard' feature")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace,
        nameguard=not args.no_nameguard
    )