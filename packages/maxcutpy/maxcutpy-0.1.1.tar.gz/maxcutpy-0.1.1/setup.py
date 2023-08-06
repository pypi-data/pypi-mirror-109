# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxcutpy']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'tqdm>=4.61.0,<5.0.0']

setup_kwargs = {
    'name': 'maxcutpy',
    'version': '0.1.1',
    'description': 'A Python Implementation of Graph Max Cut Solutions',
    'long_description': '# maxcutpy\n A Python Implementation of Graph Max Cut Solutions\n\n## Problem Statement\nThe goal of this script is to provide simple python libraries for solving the [Maximum cut problem](https://en.wikipedia.org/wiki/Maximum_cut).\n\n## Current Solvers\n\n### Universal\nThe Structure of all Solvers is the same, from an API point of view.\nThis allows for quick testing of multiple different solvers, to find the best one.\n\nIn general, the flow will look like this:\n\n    from maxcutpy import RandomMaxCut\n    import numpy as np\n\n    matrix = np.array([[0,1,1],[1,0,5],[1,5,0]])\n    random_max_cut = RandomMaxCut(matrix=matrix, seed=12345)\n\n    best_cut_vector = random_cut.batch_split()\n\n`best_cut_vector` will be a numpy array of shape `(1,n)` where n is the number of rows in the input matrix. Each number inside of `best_cut_vector` will be an integer 0 or 1, depending on if it belongs to the 0th Slice or the 1st Slice.\n\nYou can then generally check the score of this `best_cut_vector` by using the same object again:\n\n    best_cut_score = random_cut.best_cut_score\n\nAt this time, a single Solver Object is Single-Use only, meaning it gets created for a specific matrix, and provides a batch split for this matrix only. Once the result is calculated, it will be stored, and repeated calls to `batch_split()` will only return the cached result.\n\nFor now, the matrix must be in the form of a numpy adjacency matrix, but support will be added soon for networkx Graph objects, as well as helper functions to transform between the two.\n\n### RandomMaxCut\nThis solve provides a method to compare against, as all this Solver does is select a random set of vertices to cut, giving each vertex a 50% chance of occurring in a different slice of the graph.\n\n    from maxcutpy import RandomMaxCut\n    import numpy as np\n\n    matrix = np.array([[0,1,1],[1,0,5],[1,5,0]])\n    random_max_cut = RandomMaxCut(matrix=matrix, seed=12345)\n\n    best_cut_vector = random_cut.batch_split()\n\n`best_cut_vector` will be a numpy array of shape `(1,n)` where each entry is a random integer 0 or 1, with 50% probability for either event. This means this could lead to the case where no cuts are made at all, yielding a score of 0.\n',
    'author': 'trevorWieland',
    'author_email': 'trevor_wieland@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trevorWieland/maxcutpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
