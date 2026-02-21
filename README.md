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

## Image Update Watcher

`pyportainer` includes a built-in background watcher that continuously monitors your Docker containers for available image updates. It polls Portainer at a configurable interval, checks each running container's local image digest against the registry, and exposes the results for easy consumption.

### Basic usage

```python
import asyncio
from datetime import timedelta

from pyportainer import Portainer, PortainerImageWatcher


async def main() -> None:
    async with Portainer(
        api_url="http://localhost:9000",
        api_key="YOUR_API_KEY",
    ) as portainer:
        watcher = PortainerImageWatcher(
            portainer,
            interval=timedelta(hours=6),
        )

        watcher.start()

        await asyncio.sleep(30)  # Let the first check complete

        for (endpoint_id, container_id), result in watcher.results.items():
            if result.status and result.status.update_available:
                print(f"Update available for container {container_id} on endpoint {endpoint_id}")

        watcher.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

### Configuration

| Parameter     | Type          | Default  | Description                                       |
| ------------- | ------------- | -------- | ------------------------------------------------- |
| `portainer`   | `Portainer`   | —        | The Portainer client instance                     |
| `endpoint_id` | `int \| None` | `None`   | Endpoint to monitor. `None` watches all endpoints |
| `interval`    | `timedelta`   | 12 hours | How often to poll for updates                     |
| `debug`       | `bool`        | `False`  | Enable debug-level logging                        |

### Results

`watcher.results` returns a dictionary keyed by `(endpoint_id, container_id)` tuples. Each value is a `PortainerImageWatcherResult` containing:

- `endpoint_id` — the endpoint the container belongs to
- `container_id` — the container ID
- `status` — a `PortainerImageUpdateStatus` with:
  - `update_available` (`bool`) — whether a newer image is available in the registry
  - `local_digest` (`str | None`) — digest of the locally running image
  - `registry_digest` (`str | None`) — digest of the latest image in the registry

You can also inspect `watcher.last_check` to get the Unix timestamp of the most recent completed poll, or update `watcher.interval` at runtime to change the polling frequency.

### Callbacks

Register a callback to be notified automatically after each poll cycle rather than polling `watcher.results` yourself. Both sync and async callables are supported:

```python
from pyportainer.watcher import PortainerImageWatcherResult


async def on_result(result: PortainerImageWatcherResult) -> None:
    if result.status and result.status.update_available:
        print(f"Update available for {result.container_id}")


watcher.register_callback(on_result)
# Later, to remove it:
watcher.unregister_callback(on_result)
```

Callbacks receive one `PortainerImageWatcherResult` per container per cycle. Exceptions raised inside a callback are logged and do not stop the watcher.

## Documentation

The full documentation, including API reference, can be found at: [https://erwindouna.github.io/pyportainer/](https://erwindouna.github.io/pyportainer/)

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

This Python project relies on [UV][poetry] as its dependency manager,
providing comprehensive management and control over project dependencies.

### Installation

Install all packages, including all development requirements:

```bash
uv sync --all-groups && pre-commit install
```

_UV creates by default an virtual environment where it installs all necessary pip packages_.

### Pre-commit

This repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. To setup the pre-commit check, run:

```bash
uv run pre-commit install
```

And to run all checks and tests manually, use the following command:

```bash
uv run pre-commit run --all-files
```

### Testing

It uses [pytest](https://docs.pytest.org/en/stable/) as the test framework. To run the tests:

```bash
uv run pytest
```

To update the [syrupy](https://github.com/tophat/syrupy) snapshot tests:

```bash
uv run pytest --snapshot-update
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
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg
[pypi]: https://pypi.org/project/pyportainer/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/pyportainer
[releases-shield]: https://img.shields.io/github/release/erwindouna/pyportainer.svg
[releases]: https://github.com/erwindouna/pyportainer/releases
[typing-shield]: https://github.com/erwindouna/pyportainer/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/erwindouna/pyportainer/actions/workflows/typing.yaml
[uv]: https://docs.astral.sh/uv/
[pre-commit]: https://pre-commit.com
