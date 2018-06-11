import re
import os
import glob

from colorama import Fore


class Node:

    def __init__(self, key: str, args: list, comments=None, file=None, line=None):
        self.key = key
        self.comments = comments
        self.args = args
        self.file = file if isinstance(file, list) else [file]
        self.line = line if isinstance(line, list) else [line]

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(('key', self.key))

    def __repr__(self):
        return '{}=\n@args:{}\n{}\n@{}:{}\n'.format(
            self.key, self.args, self.comments, self.file, self.line)


class Parser:

    def __init__(self, regex_filter: str, comment: str):
        self.re_prog = re.compile(regex_filter)
        self.comment = comment

    def parse(self):
        """parse files into a tree"""
        tree = []
        cache = None  # a cached closure
        parsed = 0

        paths = glob.glob('./**/*', recursive=True)

        print('parsing %i files in %s' % (len(paths), os.getcwd()))

        for path in paths:
            if not os.path.isfile(path):
                continue

            # open and read file
            f = open(path, 'r')

            try:
                lines = f.readlines()
            except UnicodeDecodeError:
                pass

            for i in range(len(lines)):
                ln = lines[i]
                parsed += 1
                # parse line
                node = self.parseln(ln.strip())

                if not isinstance(node, Node):
                    # this line cannot be parsed into a node
                    # cache it for now
                    cache = node
                    continue

                if cache is not None:
                    # retrieve previous line
                    node.comments = cache()

                node.file = [os.path.basename(path)]
                node.line = [i + 1]
                tree.append(node)
            f.close()

        print('%sparsed %i keys from %i lines' %
              (Fore.GREEN, len(tree), parsed))

        return tree

    def parseln(self, ln: str):
        """Parse a single line into a node"""
        def cache():
            """Store a cached ln"""
            return ln[len(self.comment):].strip()

        if ln.startswith(self.comment):
            # this line is a comment
            return cache

        # match regex
        m = self.re_prog.match(ln)

        if m is None:
            # not a match
            return

        # cleanup match
        args = list(map(lambda x: x.strip(), m.group(1).split(',')))

        # return new Node with a key and args from the matched group
        return Node(args[0].replace('"', '').replace("'", ''), args[1:])
