# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_disqus']

package_data = \
{'': ['*'], 'sphinx_disqus': ['_static/*']}

install_requires = \
['sphinx']

extras_require = \
{'docs': ['sphinx-notfound-page',
          'sphinx-panels',
          'sphinx-rtd-theme',
          'sphinx_copybutton',
          'toml']}

setup_kwargs = {
    'name': 'sphinx-disqus',
    'version': '1.2.0',
    'description': 'Embed Disqus comments in Sphinx documents/pages.',
    'long_description': '# sphinx-disqus\n\nEmbed [Disqus](https://disqus.com) comments in Sphinx documents/pages.\n\n* Python 3.6, 3.7, 3.8, and 3.9 supported on Linux, macOS, and Windows.\n\n📖 Full documentation: https://sphinx-disqus.readthedocs.io\n\n[![Github-CI][github-ci]][github-link]\n[![Coverage Status][codecov-badge]][codecov-link]\n[![Documentation Status][rtd-badge]][rtd-link]\n[![Code style: black][black-badge]][black-link]\n[![PyPI][pypi-badge]][pypi-link]\n[![PyPI Downloads][pypi-dl-badge]][pypi-dl-link]\n\n[github-ci]: https://github.com/Robpol86/sphinx-disqus/workflows/ci/badge.svg?branch=main\n[github-link]: https://github.com/Robpol86/sphinx-disqus\n[codecov-badge]: https://codecov.io/gh/Robpol86/sphinx-disqus/branch/main/graph/badge.svg\n[codecov-link]: https://codecov.io/gh/Robpol86/sphinx-disqus\n[rtd-badge]: https://readthedocs.org/projects/sphinx-disqus/badge/?version=latest\n[rtd-link]: https://sphinx-disqus.readthedocs.io/en/latest/?badge=latest\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-link]: https://github.com/ambv/black\n[pypi-badge]: https://img.shields.io/pypi/v/sphinx-disqus.svg\n[pypi-link]: https://pypi.org/project/sphinx-disqus\n[pypi-dl-badge]: https://img.shields.io/pypi/dw/sphinx-disqus?label=pypi%20downloads\n[pypi-dl-link]: https://pypistats.org/packages/sphinx-disqus\n\n## Quickstart\n\nTo install run the following:\n\n```bash\npip install sphinx-disqus\n```\n\nTo use in Sphinx simply add to your `conf.py`:\n\n```python\nextensions = ["sphinx_disqus.disqus"]\ndisqus_shortname = "my-cool-project"\n```\n\nAlso add this to any document you wish to have comments:\n\n```rst\n.. disqus::\n```\n',
    'author': 'Robpol86',
    'author_email': 'robpol86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
