# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokenstream']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tokenstream',
    'version': '0.2.0',
    'description': 'A versatile token stream for handwritten parsers',
    'long_description': '# tokenstream\n\n[![GitHub Actions](https://github.com/vberlier/tokenstream/workflows/CI/badge.svg)](https://github.com/vberlier/tokenstream/actions)\n[![PyPI](https://img.shields.io/pypi/v/tokenstream.svg)](https://pypi.org/project/tokenstream/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tokenstream.svg)](https://pypi.org/project/tokenstream/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A versatile token stream for handwritten parsers.\n\n```python\nfrom tokenstream import TokenStream\n\ndef parse_sexp(stream: TokenStream):\n    """A basic S-expression parser."""\n    with stream.syntax(brace=r"\\(|\\)", number=r"\\d+", name=r"\\w+"):\n        brace, number, name = stream.expect(("brace", "("), "number", "name")\n        if brace:\n            return [parse_sexp(stream) for _ in stream.peek_until(("brace", ")"))]\n        elif number:\n            return int(number.value)\n        elif name:\n            return name.value\n\nprint(parse_sexp(TokenStream("(hello (world 42))")))  # [\'hello\', [\'world\', 42]]\n```\n\n## Introduction\n\nWriting recursive-descent parsers by hand can be quite elegant but it\'s often a bit more verbose than expected. In particular, handling indentation and reporting proper syntax errors can be pretty challenging. This package provides a powerful general-purpose token stream that addresses these issues and more.\n\n### Features\n\n- Define token types with regular expressions\n- The set of recognizable tokens can be defined dynamically during parsing\n- Transparently skip over irrelevant tokens\n- Expressive API for matching, collecting, peeking, and expecting tokens\n- Clean error reporting with line numbers and column numbers\n- Natively understands indentation-based syntax\n- Works well with Python 3.10+ match statements\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\npip install tokenstream\n```\n\n## Getting started\n\nYou can define tokens with the `syntax()` method. The keyword arguments associate regular expression patterns to token types. The method returns a context manager during which the specified tokens will be recognized.\n\n```python\nstream = TokenStream("hello world")\n\nwith stream.syntax(word=r"\\w+"):\n    print([token.value for token in stream])  # [\'hello\', \'world\']\n```\n\nThe token stream is iterable and will yield all the extracted tokens one after the other.\n\n## Match statements\n\nMatch statements make it very intuitive to process tokens extracted from the token stream. If you\'re using Python 3.10+ give it a try and see if you like it.\n\n```python\nfrom tokenstream import TokenStream, Token\n\ndef parse_sexp(stream: TokenStream):\n    """A basic S-expression parser that uses Python 3.10+ match statements."""\n    with stream.syntax(brace=r"\\(|\\)", number=r"\\d+", name=r"\\w+"):\n        match stream.expect_any(("brace", "("), "number", "name"):\n            case Token(type="brace"):\n                return [parse_sexp(stream) for _ in stream.peek_until(("brace", ")"))]\n            case Token(type="number") as number :\n                return int(number.value)\n            case Token(type="name") as name:\n                return name.value\n```\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org/).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n$ npm run verifytypes\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort tokenstream examples tests\n$ poetry run black tokenstream examples tests\n$ poetry run black --check tokenstream examples tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/tokenstream/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/tokenstream',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
