# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aporia_importer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'aporia[all]>=1.0.59,<2.0.0',
 'dask[complete]>=2021.6.0,<2022.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0'],
 'all': ['s3fs>=2021.6.0,<2022.0.0'],
 's3': ['s3fs>=2021.6.0,<2022.0.0']}

entry_points = \
{'console_scripts': ['aporia-importer = aporia_importer.main:main']}

setup_kwargs = {
    'name': 'aporia-importer',
    'version': '1.0.6',
    'description': 'Import data from cloud storage to Aporia',
    'long_description': "# 🏋️\u200d♀️ Aporia Importer\n![Version](https://img.shields.io/pypi/v/aporia-importer)\n![License](https://img.shields.io/github/license/aporia-ai/aporia-importer)\n\nA small utility to import ML production data from your cloud storage provider and monitor it using [Aporia's monitoring platform](https://www.aporia.com/).\n\n\n## Installation\n```\npip install aporia-importer[all]\n```\n\nIf you only wish to install the dependencies for a specific cloud provider, you can use\n```\npip install aporia-importer[s3]\n```\n\n## Usage\n```\naporia-importer /path/to/config.yaml\n```\n\n`aporia-importer` requires a config file as a parameter, see [configuration](#configuration)\n\n## Configuration\n`aporia-importer` uses a YAML configuration file.\nThere are sample configurations in the [examples](./examples) directory.\n\nCurrently, the configuration requires defining a model version schema manually - the schema is a mapping of field names to field types (see [here](https://app.aporia.com/docs/getting-started/concepts/#field-types)). You can find more details [in our docs](https://app.aporia.com/docs/getting-started/integrate-your-ml-model/#step-3-create-model-version).\n\nThe following table describes all of the configuration fields in detail:\n| Field | Required | Description\n| - | - | -\n| source | True | The path to the files you wish to upload, e.g. s3://my-bucket/my_file.csv. Glob patterns are supported.\n| format | True | The format of the files you wish to upload, see [here](#supported-data-formats)\n| token | True | Your Aporia authentication token\n| environment | True | The environment in which Aporia will be initialized (e.g production, staging)\n| model_id | True | The ID of the [model](https://app.aporia.com/docs/getting-started/concepts/#models) that the data is associated with\n| model_version.name | True | A name for the [model version](https://app.aporia.com/docs/getting-started/concepts/#model-version-schema) to create\n| model_version.type | True | The [type](https://app.aporia.com/docs/getting-started/concepts/#model-types) of the model (regression, binary, multiclass)\n| predictions | True | A mapping of [prediction fields](https://app.aporia.com/docs/getting-started/concepts/#predictions) to their field types\n| features | True | A mapping of [feature fields](https://app.aporia.com/docs/getting-started/concepts/#features) to their field types\n| raw_inputs | False | A mapping of [raw inputs fields](https://app.aporia.com/docs/getting-started/concepts/#raw-inputs) to their field types\n| aporia_host | False | Aporia server URL. Defaults to app.aporia.com\n| aporia_port | False | Aporia server port. Defaults to 443\n\n## Supported Data Sources\n* Local files\n* S3\n\n## Supported Data Formats\n* csv\n* parquet\n\n## How does it work?\n`aporia-importer` uses [dask](https://github.com/dask/dask) to load data from various cloud providers, and the [Aporia sdk](https://app.aporia.com/docs/getting-started/integrate-your-ml-model/#step-2-initialize-the-aporia-sdk) to report the data to Aporia.\n",
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aporia-ai/aporia-importer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
