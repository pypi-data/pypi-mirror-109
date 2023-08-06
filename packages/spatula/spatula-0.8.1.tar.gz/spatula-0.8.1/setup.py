# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spatula']

package_data = \
{'': ['*']}

install_requires = \
['attrs[attrs]>=20.3.0,<21.0.0',
 'click>=7.1.2,<8.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'ipython[shell]>=7.19.0,<8.0.0',
 'lxml>=4.6.2,<5.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'scrapelib>=2.0.5,<3.0.0']

entry_points = \
{'console_scripts': ['spatula = spatula.cli:cli']}

setup_kwargs = {
    'name': 'spatula',
    'version': '0.8.1',
    'description': 'A modern Python library for writing maintainable web scrapers.',
    'long_description': '# Overview\n\n*spatula* is a modern Python library for writing maintainable web scrapers.\n\nSource: [https://github.com/jamesturk/spatula](https://github.com/jamesturk/spatula)\n\nDocumentation: [https://jamesturk.github.io/spatula/](https://jamesturk.github.io/spatula/)\n\nIssues: [https://github.com/jamesturk/spatula/issues](https://github.com/jamesturk/spatula/issues)\n\n[![PyPI badge](https://badge.fury.io/py/spatula.svg)](https://badge.fury.io/py/spatula)\n[![Test badge](https://github.com/jamesturk/spatula/workflows/Test%20&%20Lint/badge.svg)](https://github.com/jamesturk/spatula/actions?query=workflow%3A%22Test+%26+Lint%22)\n\n## Features\n\n- **Page-oriented design**: Encourages writing understandable & maintainable scrapers.\n- **Not Just HTML**: Provides built in [handlers for common data formats](reference.md#pages) including CSV, JSON, XML, PDF, and Excel.  Or write your own.\n- **Fast HTML parsing**: Uses `lxml.html` for fast, consistent, and reliable parsing of HTML.\n- **Flexible Data Model Support**: Compatible with `dataclasses`, `attrs`, `pydantic`, or bring your own data model classes for storing & validating your scraped data.\n- **CLI Tools**: Offers several [CLI utilities](cli.md) that can help streamline development & testing cycle.\n- **Fully Typed**: Makes full use of Python 3 type annotations.\n\n## Installation\n\n*spatula* is on PyPI, and can be installed via any standard package\nmanagement tool:\n\n    poetry add spatula\n\nor:\n\n    pip install spatula\n\n## Example\n\nAn example of a fairly simple two-page scrape, read [A First Scraper](scraper-basics.md) for a walkthrough of how it was built.\n\n``` python\nfrom spatula import HtmlPage, HtmlListPage, CSS, XPath, SelectorError\n\n\nclass EmployeeList(HtmlListPage):\n    # by providing this here, it can be omitted on the command line\n    # useful in cases where the scraper is only meant for one page\n    source = "https://yoyodyne-propulsion.herokuapp.com/staff"\n\n    # each row represents an employee\n    selector = CSS("#employees tbody tr")\n\n    def process_item(self, item):\n        # this function is called for each <tr> we get from the selector\n        # we know there are 4 <tds>\n        first, last, position, details = item.getchildren()\n        return EmployeeDetail(\n            dict(\n                first=first.text,\n                last=last.text,\n                position=position.text,\n            ),\n            source=XPath("./a/@href").match_one(details),\n        )\n\n    def get_next_source(self):\n        try:\n            return XPath("//a[contains(text(), \'Next\')]/@href").match_one(self.root)\n        except SelectorError:\n            pass\n\n\nclass EmployeeDetail(HtmlPage):\n    def process_page(self):\n        marital_status = CSS("#status").match_one(self.root)\n        children = CSS("#children").match_one(self.root)\n        hired = CSS("#hired").match_one(self.root)\n        return dict(\n            marital_status=marital_status.text,\n            children=children.text,\n            hired=hired.text,\n            # self.input is the data passed in from the prior scrape\n            **self.input,\n        )\n\n    def process_error_response(self, exc):\n        self.logger.warning(exc)\n```\n',
    'author': 'James Turk',
    'author_email': 'dev@jamesturk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jamesturk/spatula/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
