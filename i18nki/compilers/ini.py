from i18nki.compiler import Compiler


HEADER = """; @mINI v1.0
; This file is distributed under the same license as the PACKAGE package
; compiler=i18nki v0.1
[meta]
desc=
lang=
author=NAME <EMAIL@ADDRESS>
charset=UTF-8

[strings]"""


class INI(Compiler):

    def __init__(self, separator=None):
        self.header = HEADER
        self.name = 'ini'
        self.separator = separator if separator is not None else '='

    def compile_node(self, node):
        # compile comments
        out = '\n' + self.compile_comments(node, ';')

        # compile key
        out += '%s%s\n' % (node.key, self.separator)
        return out
