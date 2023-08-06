# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quote_manager']

package_data = \
{'': ['*']}

install_requires = \
['diff-match-patch>=20181111,<20181112']

setup_kwargs = {
    'name': 'quote-manager',
    'version': '0.4.0',
    'description': 'Helper nlp library for handling non ascii quotes.',
    'long_description': '# library.quote.manager\n\nHelper nlp library for handling non ascii quotes.\n\n## Usage\n\n```python3\n\nfrom quote_manager import Quotes\n\nsentence = “That’s an ‘magic’ shoe.”\n\nquotes_sentence = Quotes(sentence)\n\nquotes_sentence.simplified\n>> "That\'s an \'magic\' shoe.\'\n\n# do stuff here...\ntransformed_sentence = transform(quotes_sentence.simplified)\n# ex. grammar correction: "That\'s a \'magic\' shoe.\'\n\nquotes_sentence.requote_modified_string(transformed_sentence)\n>> “That’s a ‘magic’ shoe.”\n```',
    'author': 'Sam Havens',
    'author_email': 'sam.havens@writer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
