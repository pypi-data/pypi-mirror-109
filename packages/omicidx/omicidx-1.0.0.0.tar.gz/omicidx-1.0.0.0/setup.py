# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omicidx',
 'omicidx.bioportal',
 'omicidx.bioportal.db',
 'omicidx.biosample.ebi',
 'omicidx.db',
 'omicidx.geo',
 'omicidx.mti',
 'omicidx.ontologies',
 'omicidx.schema',
 'omicidx.scripts',
 'omicidx.sra']

package_data = \
{'': ['*']}

install_requires = \
['Click',
 'aiohttp>=3.6.2,<4.0.0',
 'asyncpg>=0.20.1,<0.21.0',
 'asyncpgsa>=0.26.3,<0.27.0',
 'biopython==1.75',
 'boto3>=1.9,<2.0',
 'databases>=0.3.2,<0.4.0',
 'gcsfs>=0.8.0,<0.9.0',
 'prefect>=0.13.1,<0.14.0',
 'pronto>=2.0.1,<3.0.0',
 'psycopg2>=2.8.5,<3.0.0',
 'pydantic',
 'requests>=2.22,<3.0',
 'sd_cloud_utils',
 'sphinx_click>=2.3.2,<3.0.0',
 'sqlalchemy>=1.3,<2.0',
 'ujson>=1.35,<2.0']

entry_points = \
{'console_scripts': ['omicidx_tool = omicidx.scripts.cli:cli']}

setup_kwargs = {
    'name': 'omicidx',
    'version': '1.0.0.0',
    'description': 'The OmicIDX project collects, reprocesses, and then republishes metadata from multiple public genomics repositories. Included are the NCBI SRA, Biosample, and GEO databases. Publication is via the cloud data warehouse platform Bigquery, a set of performant search and retrieval APIs, and a set of json-format files for easy incorporation into other projects.',
    'long_description': '',
    'author': 'Sean Davis',
    'author_email': 'seandavi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omicidx/omicidx-parsers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
