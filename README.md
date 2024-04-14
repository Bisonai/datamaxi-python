# DataMaxi+ Python Client
[![PyPI version](https://img.shields.io/pypi/v/datamaxi)](https://pypi.python.org/pypi/datamaxi)
[![Python version](https://img.shields.io/pypi/pyversions/datamaxi)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://datamaxi.readthedocs.io/en/stable/)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the official implementation of Python client for DataMaxi+ API.
The package can be used to fetch both historical and latest data using [DataMaxi+ API](https://docs.neverest.finance/).
This package is compatible with Python v3.8+.

* [Installation](#installation)
* [Configuration](#configuration)
  * [Environment Variables](#environment-variables)
* [Quickstart](#quickstart)
* [Local Development](#local-development)
  * [Setup](#setup)
  * [Testing](#testing)
* [Links](#links)
* [Contributing](#contributing)
* [License](#license)

## Installation

```shell
pip install datamaxi
```

## Configuration

Access to DataMaxi+ is protected by API Key.
If you are interested to try DataMaxi+, you can request your API key at [business@bisonai.com](mailto:business@bisonai.com).

| Option             | Explanation                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| `api_key`          | Your API key                                                                          |
| `base_url`         | If `base_url` is not provided, it defaults to `api.neverest.finance`.                 |
| `timeout`          | Number of seconds to wait for a server response. By default requests do not time out. |
| `proxies`          | Proxy through which the request is queried                                            |
| `show_limit_usage` | Return response as dictionary including including `"limit_usage"` and `"data"` keys   |
| `show_header`      | Return response as dictionary including including `"header"` and `"data"` keys        |

### Environment Variables

You may use environment variables to configure the DataMaxi+ client to avoid any inline boilerplate.

| Env                | Description                                  |
|--------------------|----------------------------------------------|
| `NEVEREST_API_KEY` | Used instead of `api_key` if none is passed. |

## Quickstart

DataMaxi+ Python package currently includes the following clients:

* `Binance`
* `Defillama`
* `Naver`
* `Google`

All clients accept the same parameters that are described at [Configuration](#configuration) section.
First, import the clients,

```python
from datamaxi.binance import Binance
from datamaxi.defillama import Defillama
from datamaxi.naver import Naver
from datamaxi.google import Google
```

and initialize them.

```python
binance = Binance(api_key=api_key)
defillama = Defillama(api_key=api_key)
naver = Naver(api_key=api_key)
google = Google(api_key=api_key)
```

## Local Development

### Setup

If you wish to work on local development please clone/fork the git repo and use `pip install -r requirements.txt` to setup the project.

### Testing

```shell
# In case packages are not installed yet
pip install -r requirements/requirements-test.txt

python -m pytest tests/
```

## Links

* [DataMaxi+](https://datamaxiplus.com/)
* [DataMaxi+ API](https://api.neverest.finance/)
* [DataMaxi+ API Documentation](https://docs.neverest.finance/)

## Contributing

We welcome contributions!
If you discover a bug in this project, please feel free to open an issue to discuss the changes you would like to propose.

## License

[MIT License](LICENSE)
