# Home

Welcome to the documentation for PyPortainer, an asynchronous Python client for the Portainer API.

## About
This is an asynchronous Python client for the [Portainer API](https://docs.portainer.io/api-docs/). Created by [Erwin Douna](https://github.com/erwindouna). It is designed to be used with the [Portainer](https://www.portainer.io/) container management tool.
This package is a wrapper around the Portainer API, which allows you to interact with Portainer programmatically. This also includes the Docker API.

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

