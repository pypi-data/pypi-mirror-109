# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resistics']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'attotime==0.2.3',
 'loguru>=0.5.3,<0.6.0',
 'lttbc>=0.2.0,<0.3.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'prettyprinter>=0.18.0,<0.19.0',
 'pydantic>=1.8.1,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.6.2,<2.0.0',
 'tqdm>=4.61.0,<5.0.0']

setup_kwargs = {
    'name': 'resistics',
    'version': '1.0.0a0',
    'description': 'Python package for processing magnetotelluric data',
    'long_description': '## Welcome\n\nResistics is a native Python 3 package for the processing of magnetotelluric (MT) data. It incorporates standard robust processing methods and adopts a modular approach to processing which allows for customisation and future improvements to be quickly adopted.\n\n## About\n\nResistics began as a set of python classes to help analyse noisy MT timeseries data acquired in northern Switzerland through increased use of statistics and time window based features. Since then, it has grown into a MT data processing package. The name is an amalgamation of resistivty and statistics...resistics!\n\n## Audience\n\nResistics is intended for people who use magnetotelluric methods to estimate the subsurface resistivity. This may be for the purposes of furthering geological understanding, for geothermal prospecting or for other purposes.\n\n## Getting started\n\nResistics can be installed using pip,\n\n```\npython -m pip install --user resistics\n```\n\nor possibly,\n\n```\npython3 -m pip install --user resistics\n```\n\ndepending on how your Python 3 install is named.\n\nThe next step after installing is to visit www.resistics.io and read the documentation. For those unfamiliar with resistics, the features, conventions and tutorial sections are a good way to become more comfortable using the package.\n\n## Open-source\n\nResistics is available for free under the MIT licence. The resistics source code can be found in the [GitHub repository](https://github.com/resistics/resistics). Contributors are welcome.\n\n## Support and feature requests\n\nSupport and feature requests can be submitted on the in the [GitHub repository](https://github.com/resistics/resistics) page.\n',
    'author': 'Neeraj Shah',
    'author_email': 'resistics@outlook.com',
    'maintainer': 'Neeraj Shah',
    'maintainer_email': 'resistics@outlook.com',
    'url': 'https://www.resistics.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
