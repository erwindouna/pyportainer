# Home

Welcome to the documentation for PyPortainer, an asynchronous Python client for the Portainer API.

## About
This is an asynchronous Python client for the [Portainer API](https://docs.portainer.io/api-docs/). Created by [Erwin Douna](https://github.com/erwindouna). It is designed to be used with the [Portainer](https://www.portainer.io/) container management tool.
This package is a wrapper around the Portainer API, which allows you to interact with Portainer programmatically. This also includes the Docker API.
The API reference is the best place to look for all available methods and classes.

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

## Support
If you like my opensource work, you can support me via the following ways:

<a href="https://github.com/sponsors/erwindouna"><img src="https://img.shields.io/static/v1?label=Github%20Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86&style=flat-square&height=100" alt="Github Sponsor"></a>

<a href="https://buymeacoffee.com/edounae"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee"></a>

