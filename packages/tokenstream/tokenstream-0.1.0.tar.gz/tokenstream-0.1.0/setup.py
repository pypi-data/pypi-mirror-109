# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokenstream']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tokenstream',
    'version': '0.1.0',
    'description': 'A versatile token stream for handwritten parsers',
    'long_description': '# tokenstream\n\n> A versatile token stream for handwritten parsers.\n\n```python\nfrom tokenstream import TokenStream\n\ndef parse_sexp(stream: TokenStream):\n    """A basic S-expression parser."""\n    with stream.syntax(brace=r"\\(|\\)", number=r"\\d+", name=r"\\w+"):\n        brace, number, name = stream.expect(("brace", "("), "number", "name")\n        if brace:\n            return [parse_sexp(stream) for _ in stream.peek_until(("brace", ")"))]\n        elif number:\n            return int(number.value)\n        elif name:\n            return name.value\n\nprint(parse_sexp(TokenStream("(hello (world 42))")))  # [\'hello\', [\'world\', 42]]\n```\n\n## Introduction\n\nWriting recursive-descent parsers by hand can be quite elegant but it\'s often a bit more verbose than expected. In particular, handling indentation and reporting proper syntax errors can be pretty challenging. This package provides a powerful general-purpose token stream that addresses these issues and more.\n\n### Features\n\n- Define token types with regular expressions\n- The set of recognizable tokens can be defined dynamically during parsing\n- Transparently skip over irrelevant tokens\n- Expressive API for matching, collecting, peeking, and expecting tokens\n- Clean error reporting with line numbers and column numbers\n- Natively understands indentation-based syntax\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\npip install tokenstream\n```\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org/).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n$ npm run verifytypes\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort tokenstream examples tests\n$ poetry run black tokenstream examples tests\n$ poetry run black --check tokenstream examples tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/tokenstream/blob/main/LICENSE)\n',
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
