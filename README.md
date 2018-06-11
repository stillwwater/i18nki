i18nki
======

An easy to use localization file generator. `i18nki` parses localization keys from source files, then compiles them to a chosen localization format.

## Install

Local envirornment installation with [`pipsi`](https://pypi.org/project/pipsi/)

```shell
git clone https://github.com/stillwwater/i18nki
cd i18nki
pipsi install .
```

## Usage

```shell
python3 -m i18nki [-h] -i INPUT -o OUTPUT -f FILTER -c COMMENT [--compiler COMPILER]
```


| Option       | Shortcut | Description                                         | Example                                                   |
| ------------ | -------- | --------------------------------------------------- | --------------------------------------------------------- |
| `--help`     | `-h`     | Display help doc                                    | `python3 i18nki.py -h`                                    |
| `--input`    | `-i`     | Specify an input directory (files to parse)         | `-i /path/to/source/`                                     |
| `--output`   | `-o`     | Output file for compiled content                    | `-o en-US.po`                                             |
| `--filter`   | `-f`     | Regex string to match function calls in source file | ` -f ".*?_\((.*?)\).*?$" ` matches `_("my-string", arg);` |
| `--comment`  | `-c`     | Specifies the comment string of the source language | `-c "//"`                                                 |
| `--compiler` |          | Specifies which compiler to use for the output file | `--compiler ini` (see 'compilers' for more)               |



#### Compilers

+ `ini` (default)
+ `gettext` or `po`

## Example

```shell
python3 -m i18nki -i ./src -o pt-BR.ini -f ".*?Strings\.Load\((.*?)\).*?$" -c "//"
```

`src/Program.cs`

```csharp
// Print welcome message
Console.WriteLine(Strings.Load("welcome-msg", name));
Console.WriteLine(Strings.Load("exit-msg"));
exitMsg = Strings.Load("exit-msg");
```

`pt-BR.ini`

```ini
[meta]
...
[strings]
; Print welcome message
; +param+ {0}: name
; @Program.cs:2
welcome-msg=

; @Program.cs:3 @Program.cs:4
exit-msg=
```

## Custom Localization Formats

To use a custom localization format, create an object that inherits from `Compiler (compiler.py)` and override the `compile_node(self, node: Node)` function. The `Node` object has data parsed from the source files, including: `key:str`, `args:list`, `comments:str`, `file:list`, `line:list`.

Example using the `Gettext` compiler:

`compilers/gettext.py`

```python
from i18nki.compiler import Compiler

class Gettext(Compiler):
    def __init__(self):
        self.header = '# SOME DESCRIPTIVE TITLE'
        self.name = 'Gettext'

    def compile_node(self, node):
        # example output of Gettext.compile_node:
        # #, Print welcome message
        # #, param+ {0}: name
        # #: @Program.cs:2
        # msid: "welcome"
        # msgstr:

        # the compile_comments function adds comments before each key
        # with the key's parameters, location in the source and other comments
        out = '\n' + self.compile_comments(node, comment_char='#,', alt_comment_char='#:')

        # compile key
        out += 'msgid: "%s"\nmsgstr:\n' % node.key
        return out
```

A option for this compiler is then added to `__main__.py`:

```python
from i18nki.compilers import gettext

...

if compiler_choice == 'gettext' or compiler_choice == 'po':
    # change compiler option
    compiler = gettext.Gettext()
```

