from abc import ABCMeta, abstractmethod
from colorama import Fore


class Compiler:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.header = ''
        self.name = ''

    @abstractmethod
    def compile_node(self, node):
        """returns compiled version of node"""
        return str(node)

    def compile(self, tree: list, output_file: str):
        """compiles tree to output file"""
        print('compiling to %s [%s]' % (output_file, self.name))
        # merge duplicates in tree
        tree = self.merge_duplicates(tree)

        out = open(output_file, 'w')
        out.write(self.header)

        for node in tree:
            # compile node
            out.write(self.compile_node(node))

        print('%scompiled %i keys' % (Fore.GREEN, len(tree)))
        out.close()

    def merge_duplicates(self, tree: list):
        """merges duplicate nodes in tree"""
        tree_set = []

        for node in tree:
            if node in tree_set:
                # node with the same key, merge nodes
                i = tree_set.index(node)
                tree_set[i].file += node.file
                tree_set[i].line += node.line
                continue
            tree_set.append(node)

        print('%smerged %i duplicate keys' % (Fore.GREEN, len(tree) - len(tree_set)))
        return tree_set

    def compile_comments(self, node, comment_char: str, alt_comment_char=None):
        """return compiled comments for node"""
        out = ''

        if alt_comment_char is None:
            alt_comment_char = comment_char

        if node.comments is not None:
            # compile key comments
            out += '%s %s\n' % (comment_char, node.comments)

        if node.args is not None:
            # compile key positional arguments
            for i in range(len(node.args)):
                out += '%s +param+ {%i}: %s\n' % (comment_char, i, node.args[i])

        if node.file is not None and node.line is not None:
            # compile key source file and line
            out += alt_comment_char
            for i in range(len(node.file)):
                out += ' @%s:%i' % (node.file[i], node.line[i])
            out += '\n'

        return out
