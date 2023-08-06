# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cetus_cearcher', 'cetus_cearcher.third_party.singlesource']

package_data = \
{'': ['*'], 'cetus_cearcher': ['examples/*']}

install_requires = \
['requests>=2.25.1,<3.0.0',
 'rich>=10.3.0,<11.0.0',
 'typer-cli>=0.0.11,<0.0.12',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['cetus = cetus_cearcher.main:app']}

setup_kwargs = {
    'name': 'cetus-cearcher',
    'version': '0.1.0',
    'description': 'Client for the Cetus API',
    'long_description': "# `Cetus Cearcher`\n\nUnofficial CLI tool to query the Cetus API maintained by SparkIT Solutions.\n\n## Installation\n\nClone the repo and use [Typer CLI](https://typer.tiangolo.com/typer-cli/) to run\n\nor\n\n`pip install cetus-cearcher`\n\n\nOnce installed, you'll need to create a file named `config.py` in the `cetus` directory and declare two variables:\n\n|Variable |Value|\n|---|---|\n|api_url|API server including protocol ( i.e. `https://example.com` )|\n|api_key|API key obtained from the portal|\n\n## Usage\n\n```console\n$ cetus [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `example`: Show example result data\n* `search`: Search Cetus\n\n## `cetus example`\n\nShow example result data\n\n**Usage**:\n\n```console\n$ cetus example [OPTIONS] INDEX:[dns|certstream]\n```\n\n**Arguments**:\n\n* `INDEX:[dns|certstream]`: [required]\n\n**Options**:\n\n* `--raw`: Print raw output instead of pretty printed  [default: False]\n* `--help`: Show this message and exit.\n\n## `cetus search`\n\nSearch Cetus\n\n**Usage**:\n\n```console\n$ cetus search [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `certstream`: Search the Cetus Certstream index\n* `dns`: Search the Cetus DNS index\n\n### `cetus search certstream`\n\nSearch the Cetus Certstream index\n\n**Usage**:\n\n```console\n$ cetus search certstream [OPTIONS] QUERY\n```\n\n**Arguments**:\n\n* `QUERY`: Lucene formatted query.  [required]\n\n**Options**:\n\n* `--start [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: Beginning of search range. Required.  [required]\n* `--end [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: End of search range. If omitted, end == now  [default: 2021-06-10T17:11:20]\n* `--raw`: Print raw output instead of pretty printed  [default: False]\n* `--metadata`: Include metadata in output  [default: False]\n* `--help`: Show this message and exit.\n\n### `cetus search dns`\n\nSearch the Cetus DNS index\n\n**Usage**:\n\n```console\n$ cetus search dns [OPTIONS] QUERY\n```\n\n**Arguments**:\n\n* `QUERY`: Lucene formatted query.  [required]\n\n**Options**:\n\n* `--start [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: Beginning of search range. Required.  [required]\n* `--end [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`: End of search range. If omitted, end == now  [default: 2021-06-10T17:11:20]\n* `--raw`: Print raw output instead of pretty printed  [default: False]\n* `--metadata`: Include metadata in output  [default: False]\n* `--help`: Show this message and exit.\n",
    'author': 'Kory Kyzar',
    'author_email': 'k2@korrosivesecurity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
