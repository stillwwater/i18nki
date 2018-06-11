from i18nki.compiler import Compiler


HEADER = """# SOME DESCRIPTIVE TITLE
# Copyright (C) YEAR
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION"
"POT-Creation-Date: 2008-02-06 16:25-0500"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>"
"Language-Team: LANGUAGE <LL@li.org>"
"MIME-Version: 1.0"
"Content-Type: text/plain; charset=CHARSET"
"Content-Transfer-Encoding: ENCODING"
"""


class Gettext(Compiler):

    def __init__(self):
        self.header = HEADER
        self.name = 'Gettext'

    def compile_node(self, node):
        out = '\n' + \
            self.compile_comments(node, '#,', '#:')

        # compile key
        out += 'msgid: "%s"\nmsgstr:\n' % node.key
        return out
