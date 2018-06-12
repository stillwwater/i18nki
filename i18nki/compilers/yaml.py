from i18nki.compiler import Compiler


HEADER = """# @YAML v1.0
# This file is distributed under the same license as the PACKAGE package
# compiler: i18nki v0.1

---
desc:
lang:
author: NAME <EMAIL@ADDRESS>
charset: UTF-8
---
"""


class YAML(Compiler):

    def __init__(self):
        self.header = HEADER
        self.name = 'csv'

    def compile_node(self, node):
        out = ''

        # compile comments
        out = '\n' + self.compile_comments(node, '#')

        # compile key
        out += '%s:\n' % node.key
        return out
