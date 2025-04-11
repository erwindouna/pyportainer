<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![PyPi Downloads][downloads-shield]][downloads-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]
[![Open in Dev Containers][devcontainer-shield]][devcontainer]

[![Build Status][build-shield]][build-url]
[![Typing Status][typing-shield]][typing-url]
[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]


Asynchronous Python client for Python Portainer.

## About

This is an asynchronous Python client for the [Portainer API](https://docs.portainer.io/api-docs/). It is designed to be used with the [Portainer](https://www.portainer.io/) container management tool.
This package is a wrapper around the Portainer API, which allows you to interact with Portainer programmatically.

In it's current stage it's still in development and not all endpoints are implemented yet.

## Installation

```bash
pip install pyportainer
```

### Example

```python
import asyncio

from pyportainer import Portainer


async def main() -> None:
    """Run the example."""
    async with Portainer(
        api_url="http://localhost:9000",
        api_key="YOUR_API_KEY",
    ) as portainer:
        endpoints = await portainer.get_endpoints()
        print("Portainer Endpoints:", endpoints)


if __name__ == "__main__":
    asyncio.run(main())
```

More examples can be found in the [examples folder](./examples/).

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

The simplest way to begin is by utilizing the [Dev Container][devcontainer]
feature of Visual Studio Code or by opening a CodeSpace directly on GitHub.
By clicking the button below you immediately start a Dev Container in Visual Studio Code.

[![Open in Dev Containers][devcontainer-shield]][devcontainer]

This Python project relies on [Poetry][poetry] as its dependency manager,
providing comprehensive management and control over project dependencies.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]

### Installation

Install all packages, including all development requirements:

```bash
poetry install
```

_Poetry creates by default an virtual environment where it installs all
necessary pip packages_.

### Pre-commit

This repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. To setup the pre-commit check, run:

```bash
poetry run pre-commit install
```

And to run all checks and tests manually, use the following command:

```bash
poetry run pre-commit run --all-files
```

### Testing

It uses [pytest](https://docs.pytest.org/en/stable/) as the test framework. To run the tests:

```bash
poetry run pytest
```

To update the [syrupy](https://github.com/tophat/syrupy) snapshot tests:

```bash
poetry run pytest --snapshot-update
```

## License

MIT License

Copyright (c) 2025 Erwin Douna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


<!-- LINKS FROM PLATFORM -->


<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/erwindouna/pyportainer/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/erwindouna/pyportainer/actions/workflows/tests.yaml
[codecov-shield]: https://codecov.io/gh/erwindouna/pyportainer/branch/main/graph/badge.svg?token=TOKEN
[codecov-url]: https://codecov.io/gh/erwindouna/pyportainer
[commits-shield]: https://img.shields.io/github/commit-activity/y/erwindouna/pyportainer.svg
[commits-url]: https://github.com/erwindouna/pyportainer/commits/main
[devcontainer-shield]: https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode
[devcontainer]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/erwindouna/pyportainer
[downloads-shield]: https://img.shields.io/pypi/dm/pyportainer
[downloads-url]: https://pypistats.org/packages/pyportainer
[last-commit-shield]: https://img.shields.io/github/last-commit/erwindouna/pyportainer.svg
[license-shield]: https://img.shields.io/github/license/erwindouna/pyportainer.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/TOKEN/maintainability
[maintainability-url]: https://codeclimate.com/github/erwindouna/pyportainer/maintainability
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[pypi]: https://pypi.org/project/pyportainer/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/pyportainer
[releases-shield]: https://img.shields.io/github/release/erwindouna/pyportainer.svg
[releases]: https://github.com/erwindouna/pyportainer/releases
[typing-shield]: https://github.com/erwindouna/pyportainer/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/erwindouna/pyportainer/actions/workflows/typing.yaml

[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
