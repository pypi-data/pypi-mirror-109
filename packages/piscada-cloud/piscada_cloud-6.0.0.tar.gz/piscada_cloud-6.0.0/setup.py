# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piscada_cloud']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'piscada-cloud',
    'version': '6.0.0',
    'description': 'Library for the Piscada Cloud including authentication and data access.',
    'long_description': '# Picada Cloud\n\nLibrary for the Piscada Cloud including authentication and data access.\n\n## Features\n\n- Login to Piscada Cloud and retrieve credentials\n- Persist credentialss locally\n- Read historic values for multiple tags as a Pandas DataFrame\n- Possible apply time-based linear interpolation to measurements\n- Utils to add fractional representations of periods: day, week, year\n\n## Install\n\nInstall from PyPI:\n\n```shell\npip install piscada-cloud\n```\n\nor\n\n```shell\npoetry add piscada-cloud\n```\n\nInstall from local source:\n\n```shell\npip install --editable path/to/piscada_cloud\n```\n\nor\n\n```shell\npoetry add path/to/piscada_cloud\n```\n\n## Usage\n\n### Authentication\n\nTo log-in interactively and persist the retrieved credentials on disk (under `$HOME/.piscada_credentials`) simply run:\n\n```shell\npython -m piscada_cloud.auth\n```\n\nor\n\n```shell\npoetry run python -m piscada_cloud.auth\n```\n\nAny future invocation, e.g. `credentials = piscada_cloud.auth.persisted_login()` will return the credentials on disk without user interaction.\n\n`credentials = piscada_cloud.auth.login(username, password, host)` can be used to retrieve the credentials programmatically.\n\n### Getting Data\n\nThe credentials retrieved through the login can be used to get the host and acccesss-token for the historical data API:\n\n```python\nfrom piscada_cloud import auth\n\ncredentials = auth.login_persisted()\nhost, token = auth.get_historian_credentials(credentials)\n```\n\nThe host and token can be used to retrieve historic data as a Pandas DataFrame.\nThe `get_historic_values` method takes a row of parameters:\n\n- controller: e.g. `0798ac4a-4d4f-4648-95f0-12676b3411d5`\n- start date as ISO8601 string: e.g. `2019-08-01T00:00Z`\n- end date as ISO8601 string: e.g. `2019-08-01T00:00Z`\n- a list of tags: e.g. `["oBU136003RT90_MV|linear", "oBU136003QD40_A1"]` which can optionally include the suffix `|linear` to enable linear time-based interpolation on this tag.\n- Endpoint to which we send the historian queries. e.g. `historian.piscada.online`. Optional.\n- Access token, associated with the endpoint, used for authentication. Optional.\n\n```python\nfrom piscada_cloud.data import get_historic_values\n\ndata = get_historic_values(\n    "0798ac4a-4d4f-4648-95f0-12676b3411d5",\n    "2019-08-01T00:00Z",\n    "2019-08-31T23:59Z",\n    [\n        "oBU136003RT90_MV|linear",\n        "oBU136003QD40_A1",\n    ],\n)\n```\n\n## Write Data\n\nIn this example the column `oCU135001RT90_MV` is selected and the average value is calculated using the method `.mean()`.\n\nTo write the result back to the Piscada Cloud, the `data` module offers the `write_value` function. It takes three arguments: `controller_id`, `target_tag`, and `value`.\n\nThe `target_tag` must use the prefix `py_` as this is the only namespace allowed for writing data via the API.\n\n```python\nmean = data_frame["oCU135001RT90_MV"].mean()\nprint(mean)\nresponse = write_value("0798ac4a-4d4f-4648-95f0-12676b3411d5", "py_oCU135001RT90_MV_1h_mean", mean)\nif response.ok:\n    print("OK")\nelse:\n    print(response.text)\n```\n\nThe `response` returned by the `write_value` method allows to check if the writing of data was successful `response.ok == True`.\n\n### Manipulations\n\nIn order to support analysis in the context of periodic patters, the `manipulations` allow you to add fractional representations of day, week, and year as additional columns in the DataFrame:\n\n- 00:00:00 -> 0.0 --- 23:59:59 -> 1.0\n- Monday 00:00:00 -> 0.0 --- Sunday 23:59:59 -> 1.0\n- 1st Jan. 00:00:00 -> 0.0 --- 31st Dec. 23:59:59 -> 1.0\n\n```python\nfrom piscada_cloud import manipulations\n\nmanipulations.add_weekdays(data)\nmanipulations.add_day_fraction(data)\nmanipulations.add_week_fraction(data)\nmanipulations.add_year_fraction(data)\n```\n\n## Development\n\nEnable the provided git pre commit hook: `ln -s ./qa.sh .git/hooks/pre-commit`\n\n## Requirements\n\nThe package will support the two latest version of Python.\n\n## Authors\n\n- Tim Jagenberg [tim.jagenberg@piscada.com](mailto:tim.jagenberg@piscada.com)\n- Filip Henrik Larsen [filip.larsen@piscada.com](mailto:filip.larsen@piscada.com)\n\n## License\n\n© Piscada AS 2019\n',
    'author': 'Tim Jagenberg',
    'author_email': 'tim.jagenberg@piscada.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://piscada.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
