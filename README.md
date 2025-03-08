# DataMaxi+ Python SDK

[![PyPI version](https://img.shields.io/pypi/v/datamaxi)](https://pypi.python.org/pypi/datamaxi)
[![Python version](https://img.shields.io/pypi/pyversions/datamaxi)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://datamaxi.readthedocs.io/en/stable/)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the official implementation of Python SDK for DataMaxi+ API.
The package can be used to fetch both historical and latest data using [DataMaxi+ API](https://docs.datamaxiplus.com/).
This package is compatible with Python v3.8+.

- [Installation](#installation)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
- [Quickstart](#quickstart)
- [Local Development](#local-development)
- [Tests](#tests)
- [Links](#links)
- [Contributing](#contributing)
- [License](#license)

## Installation

```shell
pip3 install datamaxi
```

## Configuration

Private API endpoints are protected by an API key.
You can get the API key upon registering at https://datamaxiplus.com/auth.

| Option             | Explanation                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| `api_key`          | Your API key                                                                          |
| `base_url`         | If `base_url` is not provided, it defaults to `https://api.datamaxiplus.com`.         |
| `timeout`          | Number of seconds to wait for a server response. By default requests do not time out. |
| `proxies`          | Proxy through which the request is queried                                            |
| `show_limit_usage` | Return response as dictionary including `"limit_usage"` and `"data"` keys             |
| `show_header`      | Return response as dictionary including `"header"` and `"data"` keys                  |

### Environment Variables

You may use environment variables to configure the SDK to avoid any inline boilerplate.

| Env                | Description                                  |
| ------------------ | -------------------------------------------- |
| `DATAMAXI_API_KEY` | Used instead of `api_key` if none is passed. |

## Quickstart

DataMaxi+ Python package currently includes the following clients:

- `Datamaxi`
- `Naver`

All clients accept the same parameters that are described at [Configuration](#configuration) section.
First, import the clients,

```python
# Main client to access crypto trading data
from datamaxi.datamaxi import Datamaxi

# Trend
from datamaxi.naver import Naver
```

and initialize them.

```python
# Main client
maxi = Datamaxi(api_key=api_key)

# Trend
naver = Naver(api_key=api_key)
```

## Local Development

If you wish to work on local development please clone/fork the git repo and use `pip install -r requirements.txt` to setup the project.

## Tests

```shell
# In case packages are not installed yet
pip3 install -r requirements/requirements-test.txt

python3 -m pytest tests/
```


## Links

- [Official Website](https://datamaxiplus.com/)
- [Documentation](https://docs.datamaxiplus.com/)

## Contributing

We welcome contributions!
If you discover a bug in this project, please feel free to open an issue to discuss the changes you would like to propose.

## License

[MIT License](LICENSE)
