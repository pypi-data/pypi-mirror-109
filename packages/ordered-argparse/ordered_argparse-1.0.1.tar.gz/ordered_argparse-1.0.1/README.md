# ordered_argparse

Version of Python's standard library's `argparse` which also remembers the order of command line arguments.

## Installation

Install with `pip install ordered_argparse`.

## Usage

Create an instance of `ArgumentParser` as usual. Use `namespace=ordered_argparse.OrderedNamespace()`. Access arguments in declaration order by calling parser's `.ordered()` method.

```python
import ordered_argparse

parser = ordered_argparse.ArgumentParser()
parser.add_argument("--foo", action="store_true", help="foo")
parser.add_argument("--bar", action="store_true", help="bar")

# Use Ordered_Namespace when parsing CLI arguments
args = parser.parse_args(["--foo", "--bar"], namespace=ordered_argparse.OrderedNamespace())

# Access ordered arguments by calling .ordered()
for arg in args.ordered():
    print(f"{arg}")
```

## Compatibility with argcomplete

ordered_argparse only works with `argcomplete` as long as you don't use subparsers. If you use subparsers, you need `ordered_argcomplete`.

