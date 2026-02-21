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

## Image Update Watcher

`pyportainer` comes with a built-in background watcher that continuously monitors your running containers for available image updates. It polls Portainer at a configurable interval and exposes results without blocking your application.

```python
import asyncio
from datetime import timedelta

from pyportainer import Portainer, PortainerImageWatcher
from pyportainer.watcher import PortainerImageWatcherResult


async def on_update(result: PortainerImageWatcherResult) -> None:
    """Handle an image update notification."""
    if result.status and result.status.update_available:
        print(f"Update available for container {result.container_id}")


async def main() -> None:
    """Run the example."""
    async with Portainer(
        api_url="http://localhost:9000",
        api_key="YOUR_API_KEY",
    ) as portainer:
        watcher = PortainerImageWatcher(portainer, interval=timedelta(hours=6))
        watcher.register_callback(on_update)
        watcher.start()

        await asyncio.sleep(60)  # Run for a while

        watcher.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

See the [Image Update Watcher](watcher.md) page for the full documentation, including all configuration options, callback usage, and runtime controls.

## Event Listener

`pyportainer` also includes a `PortainerEventListener` that maintains a **persistent streaming connection** to the Docker events endpoint. Unlike the image watcher, it reacts in real time as events occur — no polling interval needed.

```python
import asyncio

from pyportainer import Portainer, PortainerEventListener
from pyportainer.listener import PortainerEventListenerResult


async def on_event(result: PortainerEventListenerResult) -> None:
    """Handle an incoming Docker event."""
    print(f"[endpoint {result.endpoint_id}] {result.event.type} {result.event.action}")


async def main() -> None:
    """Run the example."""
    async with Portainer(
        api_url="http://localhost:9000",
        api_key="YOUR_API_KEY",
    ) as portainer:
        listener = PortainerEventListener(portainer, event_types=["container"])
        listener.register_callback(on_event)
        listener.start()

        await asyncio.sleep(60)

        listener.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

See the [Event Listener](listener.md) page for the full documentation, including filtering, callbacks, reconnect behaviour, and how to query events directly.

## Support

If you like my opensource work, you can support me via the following ways:

<a href="https://github.com/sponsors/erwindouna"><img src="https://img.shields.io/static/v1?label=Github%20Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86&style=flat-square&height=100" alt="Github Sponsor"></a>

<a href="https://buymeacoffee.com/edounae"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee"></a>
