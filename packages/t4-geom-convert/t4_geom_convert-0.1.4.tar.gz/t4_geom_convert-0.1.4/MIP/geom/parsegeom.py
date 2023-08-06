#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkgutil import get_data
import re
from codecs import open
import tatsu
from tatsu.ast import AST

from .semantics import GeomSemantics

from os import path


grammar = get_data('MIP.geom.grammars', 'geom.ebnf').decode('utf-8')
parser = tatsu.compile(grammar)  # , left_recurion=False)

# patterns to replace space denoting intersection with '*'
re_union = re.compile('\s*:\s*')
re_pareno = re.compile('\(\s*')
re_parenc = re.compile('\s*\)')
re_spaces = re.compile('\s+')
re_compl = re.compile('#(\d+)')


def normalize(geom):
    """
    Replace spaces denoting intersection with `*`.

    Also replace '#' denoting complement with '_' .
    """
    g = geom.strip()

    # remove spaces around ':' operator
    g = re_union.sub(':', g)
    # remove spaces after '(' and before ')'
    g = re_pareno.sub('(', g)
    g = re_parenc.sub(')', g)
    # replace one or more spaces with exactly one ' '.
    g = re_spaces.sub('*', g)

    g = re_compl.sub(r'^(\1)', g)
    g = g.replace('#', '_')
    return g


def get_ast(geom):
    if 'like' in geom.lower():
        return geom.split()[1]
    g = normalize(geom)
    ast = parser.parse(g, semantics=GeomSemantics())
    return ast


def modify_ast(ast, d):
    """
    Assume ast is a recursive tuple with integers as terminal elements (signed
    surfaces).  Replace surfaces with their card representation, prepended with
    sign.
    """
    def mapping(e):
        return modify_ast(e, d)

    print('***', repr(ast))

    if isinstance(ast, tuple):
        return list(map(mapping, ast))
    elif isinstance(ast, str):
        return ast
    else:
        return ast > 0, d[abs(ast)]

    return list(map(mapping, ast))


if __name__ == '__main__':
    from sys import argv
    from mcrp_splitters import InputSplitter
    from mip.utils import shorten

    input = InputSplitter(argv[1])

    n = 0
    for c in input.cards(blocks='c', skipcomments=True):
        name, mat, geom, opts = c.parts()
        print(n, c.position, name, shorten(geom))
        ast = get_ast(geom)
        print(repr(ast))
        n += 1
        if n >= 100:
            break
