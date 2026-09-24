"""
    Lexer for the ACL2 language.

    Derived from the elisp lexer distributed with Pygments.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :copyright: Copyright 2025-2026 Grant Jurgensen, Kestrel Institute.
    :license: BSD 2-Clause, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, include, bygroups, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Literal, Error, Whitespace

from pygments.lexers.python import PythonLexer

from pygments.lexers._scheme_builtins import scheme_keywords, scheme_builtins

__all__ = ['ACL2Lexer']


# Based on the elisp lexer
class ACL2Lexer(RegexLexer):
    """
    An ACL2 lexer.
    """
    name = 'ACL2'
    aliases = ['acl2']
    filenames = ['*.lisp']
    mimetypes = ['text/x-acl2']
    url = 'https://acl2.org'

    flags = re.IGNORECASE | re.MULTILINE

    # couple of useful regexes

    # characters that are not macro-characters and can be used to begin a symbol
    nonmacro = r'\\.|[\w!$%&*+-/<=>?@^{}~|]'
    constituent = nonmacro + '|[#.:]'
    terminated = r'(?=[ "()\]\'\n,;`])'  # whitespace or terminating macro characters

    # symbol token, reverse-engineered from hyperspec
    # Take a deep breath...
    symbol = rf'((?:{nonmacro})(?:{constituent})*)'

    macros = {
        'case', 'defchoose', 'define', 'definductive', 'defmacro', 'defun',
        'defun-sk', 'define-sk', 'defstub',
        'mutual-recursion',
        'fty::deftagsum', 'fty::deftypes',
        'defrule', 'defruled', 'defrulel',
        'encapsulate', 'flet', 'lambda', 'local', 'defthm',
        'defequiv',
        'declare', 'ignore', 'xargs'
    }

    special_forms = {
        # 'and',
        'b*',
        'cond', 'defconst', 'if', 'let', 'let*',
        # 'or',
        'prog2$', 'progn',
        'quote',
        'forall',
        'exists',
    }

    builtin_function = {
        '%', '*', '+', '-', '/', '/=', '1+', '1-', '<', '<=', '=', '>', '>=',
        'and', 'or',
        'booleanp',
        'acl2-count',
        'cons', 'consp', 'car', 'cdr',
        'evenp', 'oddp',
        'list', 'list*',
        'equal', 'eql', 'eq',
        'floatp', 'floor',
        'implies',
        'not',
        'nfix',
        'zp',
        'natp',
        'apply$',
    }

    lambda_list_keywords = {
        '&key', '&optional', '&rest', '&whole',
    }

    def get_tokens_unprocessed(self, text):
        stack = ['root']
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name.Variable:
                if value in ACL2Lexer.builtin_function:
                    yield index, Name.Function, value
                    # yield index, Name.Exception, value
                    continue
                if value in ACL2Lexer.special_forms:
                    yield index, Keyword, value
                    continue
                if value in ACL2Lexer.macros:
                    yield index, Name.Builtin, value
                    # yield index, Name.Exception, value
                    continue
                if value in ACL2Lexer.lambda_list_keywords:
                    yield index, Keyword.Pseudo, value
                    continue
            yield index, token, value

    tokens = {
        'root': [
            default('body'),
        ],
        'body': [
            # whitespace
            (r'\s+', Whitespace),

            # single-line comment
            (r';.*$', Comment.Single),

            # strings and characters
            (r'"', String, 'string'),
            (r'\?([^\\]|\\.)', String.Char),
            # quoting
            (r":" + symbol, Name.Builtin),
            (r"::" + symbol, String.Symbol),
            (r"'" + symbol, String.Symbol),
            (r"'", Operator),
            (r"`", Operator),

            # decimal numbers
            (r'[-+]?\d+\.?' + terminated, Number.Integer),
            (r'[-+]?\d+/\d+' + terminated, Number),
            (r'[-+]?(\d*\.\d+([defls][-+]?\d+)?|\d+(\.\d*)?[defls][-+]?\d+)' +
             terminated, Number.Float),

            # vectors
            (r'\[|\]', Punctuation),

            # uninterned symbol
            (r'#:' + symbol, String.Symbol),

            # read syntax for char tables
            (r'#\^\^?', Operator),

            # function shorthand
            (r'#\'', Name.Function),

            # binary rational
            (r'#[bB][+-]?[01]+(/[01]+)?', Number.Bin),

            # octal rational
            (r'#[oO][+-]?[0-7]+(/[0-7]+)?', Number.Oct),

            # hex rational
            (r'#[xX][+-]?[0-9a-fA-F]+(/[0-9a-fA-F]+)?', Number.Hex),

            # radix rational
            (r'#\d+r[+-]?[0-9a-zA-Z]+(/[0-9a-zA-Z]+)?', Number),

            # reference
            (r'#\d+=', Operator),
            (r'#\d+#', Operator),

            # special operators that should have been parsed already
            (r'(,@|,|\.|:)', Operator),

            # special constants
            (r'(t|nil)' + terminated, Name.Constant),

            # functions and variables
            (r'\*' + symbol + r'\*', Name.Variable.Global),
            (symbol, Name.Variable),

            # parentheses
            (r'#\(', Operator, 'body'),
            (r'\(', Punctuation, 'body'),
            (r'\)', Punctuation, '#pop'),
        ],
        'string': [
            (r'[^"\\`]+', String),
            (rf'`{symbol}\'', String.Symbol),
            (r'`', String),
            (r'\\.', String),
            (r'\\\n', String),
            (r'"', String, '#pop'),
        ],
    }
