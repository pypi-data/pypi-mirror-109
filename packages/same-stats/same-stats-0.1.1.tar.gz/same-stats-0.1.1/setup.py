# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['same_stats']

package_data = \
{'': ['*'], 'same_stats': ['seed_datasets/*']}

install_requires = \
['PyTweening==1.0.3',
 'matplotlib>=3.4.2,<4.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'tqdm>=4.61.1,<5.0.0']

setup_kwargs = {
    'name': 'same-stats',
    'version': '0.1.1',
    'description': 'A tool to create datasets with different graphs but the same statistics',
    'long_description': '# Same Stats Different Graphs\n\nA Python tool to create datasets whose graphs are different from one another but their statistics are the same. This is a modified version of the code provided at [Autodesk](https://www.autodesk.com/research/publications/same-stats-different-graphs). \n\nThis library makes it easy for you to turn one shape to another and create GIFs for this transformation on the command line.\n\n## Installation\nTo install the package, type:\n```bash\npip install same-stats\n```\n\n## Usage\nTo turn a dinosaur shape into a bull eye shape, type:\n```bash\npython -m same_stats --shape_start=dino --shape_end=bullseye\n```\nAnd a GIF like below will be saved to the `gifs` directory as `dino_bullseye.gif`:\n![gif](https://github.com/khuyentran1401/same-stats-different-graphs/blob/master/gifs/dino_bullseye.gif?raw=True)\n\nArgument options:\n* `--shape_start`: Shape start. \n    Options: `dino`, `rando`, `slant`, `big_slant`\n* `--shape_end`: Target shape. \n    Options: `x`, `h_lines`, `v_lines`, `wide_lines`, `high_lines`,`slant_up`, `slant_down`, `center`, `star`, `down_parab`, `circle`,`bullseye`, `dots`\n* `--iters`: Number of iteration\n* `--decimals`: Number of decimals\n* `--frames`: Number of frames\n\n\n',
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/same-stats-different-graphs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
