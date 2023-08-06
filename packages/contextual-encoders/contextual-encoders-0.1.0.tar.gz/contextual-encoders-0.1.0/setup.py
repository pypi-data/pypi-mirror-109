# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextual_encoders']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0', 'numpy>=1.19,<2.0', 'scikit-learn>=0.24,<0.25']

setup_kwargs = {
    'name': 'contextual-encoders',
    'version': '0.1.0',
    'description': 'A library of sklearn compatible contextual categorical variable encoders',
    'long_description': '# Contextual Encoders\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)\n![Python: >= 3.7](https://img.shields.io/badge/python-^3.7-blue)\n[![Documentation Status](https://readthedocs.org/projects/contextual-encoders/badge/?version=latest)](https://contextual-encoders.readthedocs.io/en/latest/?badge=latest)\n[![Python Tests](https://github.com/StuttgarterDotNet/contextual-encoders/actions/workflows/python.yml/badge.svg?branch=main)](https://github.com/StuttgarterDotNet/contextual-encoders/actions/workflows/python.yml)\n\nContextual Encoders is a library of [scikit-learn](https://scikit-learn.org/stable) compatible contextual variable encoders.\n\nThe documentation can be found here: [ReadTheDocs](https://contextual-encoders.readthedocs.io).\n\nThis package uses Poetry ([documentation](https://python-poetry.org/docs/)).\n\n## What are contextual variables?\nContextual variables are numerical or categorical variables, that underlie a certain context or relationship.\nExamples are the days of the week, that have a hidden graph structure:\n\n<p align="center">\n<img src="https://raw.githubusercontent.com/StuttgarterDotNet/contextual-encoders/main/docs/_static/weekdays.svg" alt="">\n</p>\n\nWhen encoding these categorical variables with a simple encoding strategy such as <em>One-Hot-Encoding</em>, the hidden structure will be neglected.\nHowever, when the context can be specified, this additional information can be put it into the learning procedure to increase the performance of the learning model.\nThis is, where Contextual Encoders come into place.\n\n## Principle\nThe step of encoding contextual variables is split up into four sub-steps:\n\n1) Define the context\n2) Define the measure\n3) Calculate the (dis-) similarity matrix\n4) Map the distance matrix to euclidean vectors\n\nSetp 4. is optional and depends on the ML technique that uses the encoding.\nFor example, [Agglomerative Clustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html) \ntechniques do not require euclidean vectors, they can use a dissimilarity matrix directly.\n\n## Basic Usage\n\nThe code below demonstrates the basic usage of the library.\nHere, a simple dataset with 10 features is used.\n\n```python\nfrom contextual_encoders import ContextualEncoder, GraphContext, PathLengthMeasure\nimport numpy as np\n\n\n# Create a sample dataset\nx = np.array(["Fri", "Tue", "Fri", "Sat", "Mon", "Tue", "Wed", "Tue", "Fri", "Fri"])\n\n# Step 1: Define the context\nday = GraphContext("day")\nday.add_concept("Mon", "Tue")\nday.add_concept("Tue", "Wed")\nday.add_concept("Wed", "Thur")\nday.add_concept("Thur", "Fri")\nday.add_concept("Fri", "Sat")\nday.add_concept("Sat", "Sun")\nday.add_concept("Sun", "Mon")\n\n# Step 2: Define the measure\nday_measure = PathLengthMeasure(day)\n\n# Step 3+4: Calculate (Dis-) similarity Matrix\n#           and map to euclidean vectors\nencoder = ContextualEncoder(day_measure)\nencoded_data = encoder.fit_transform(x)\n\nsimilarity_matrix = encoder.get_similarity_matrix()\ndissimilarity_matrix = encoder.get_dissimilarity_matrix()\n```\n\nThe output of the code is visualized below.\nThe graph-based structure can be clearly seen when the euclidean data points are plotted.\nNote, that only five points can be seen, because the days "Thur" and "Sun" are missing in the dataset.\n\nSimilarity Matrix          |  Dissimilarity Matrix     |  Euclidean Data Points\n:-------------------------:|:-------------------------:|:-------------------------:\n![](https://github.com/StuttgarterDotNet/contextual-encoders/blob/main/docs/_static/readme_example_similarity_matrix.png?raw=true)  |  ![](https://github.com/StuttgarterDotNet/contextual-encoders/blob/main/docs/_static/readme_example_dissimilarity_matrix.png?raw=true)  | ![](https://github.com/StuttgarterDotNet/contextual-encoders/blob/main/docs/_static/readme_example_euclidean_data_points.png?raw=true)\n\nMore complicated examples can be found in the [documentation](https://contextual-encoders.readthedocs.io/en/latest/examples.html).\n\n## Notice\nThe [Preprocessing](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing) module from scikit-learn offers multiple encoders for categorical variables.\nThese encoders use simple techniques to encode categorical variables into numerical variables.\nAdditionally, the [Category Encoders](http://contrib.scikit-learn.org/category_encoders) package offers more sophisticated encoders for the same purpose.\nThis package is meant to be used as an extension to the previous two packages in the cases, when the context of a numerical or categorical variable can be specified.\n\nThis project is currently in the developer stage.\n',
    'author': 'Daniel Fink',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://contextual-encoders.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
