# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fluidtopics', 'fluidtopics.markdown']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click-log>=0.3,<0.4',
 'click>=7,<8',
 'fluidtopics>=1.0.3,<2.0.0',
 'importlib-metadata>=3,<4',
 'lxml>=4.5.1,<5.0.0',
 'python-slugify>=4.0.0,<5.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['md2ft = fluidtopics.markdown.cli:cli']}

setup_kwargs = {
    'name': 'fluidtopics-markdown',
    'version': '0.9.3',
    'description': 'A Markdown to FluidTopics command line tool',
    'long_description': '# Markdown to Fluitopics command line tool\n\nThe idea of this tool is to be able to collect documentation written\nas markdown files in a various places in a project and push it to\na [Fluitopics](https://www.fluidtopics.com/) portal.\n\nThe tool uses the FTML upload capability:\n\n- https://doc.fluidtopics.com/r/Upload-FTML-Content-to-Fluid-Topics/Configure-FTML-Content\n\n## Features\n\n- Collect any markdown file (.md) contained in a project\n- Be able to select public vs internal content from [metadata contained\n  in the markdown files](https://stackoverflow.com/questions/44215896/markdown-metadata-format).\n- Build the FT TOC (ftmap) from metadata contained in the markdown files\n\n## Documentation\n\nYou can find some explanations on how md2ft works [here](https://doc.fluidtopics.com/r/Technical-Notes/Markdown-to-Fluid-Topics-md2ft).\n',
    'author': 'Antidot Opensource',
    'author_email': 'opensource@antidot.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
