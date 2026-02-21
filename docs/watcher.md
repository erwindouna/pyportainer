# Image Update Watcher

`pyportainer` comes with a built-in background watcher: `PortainerImageWatcher`. The watcher can continuously monitor your running Docker containers for available image updates.

It polls Portainer at a configurable interval, compares the local image digest of each running container against the digest in the registry, and stores the results so your application can react to available updates without blocking.

## How it works

1. On `start()`, a background asyncio task is created.
2. The first check runs immediately, then repeats after each configured `interval`.
3. For every endpoint (or a specific one), the watcher fetches all running containers, deduplicates by image, and concurrently calls `container_image_status()` for each unique image.
4. Results are stored internally and exposed via `watcher.results`.
5. Errors for individual containers or endpoints are logged but never stop the polling loop.

## Installation

No extra dependencies are needed, the watcher is part of the core `pyportainer` package and runs on `asyncio`.

## Basic usage

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

        # Depending on the registires it may take some time for the first check to complete
        # So we wait a bit before accessing results
        await asyncio.sleep(timedelta(minutes=1))
        for (endpoint_id, container_id), result in watcher.results.items():
            if result.status and result.status.update_available:
                print(f"Update available for container {container_id} on endpoint {endpoint_id}")

        watcher.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

## Watching a specific endpoint

Pass `endpoint_id` to limit monitoring to a single Portainer endpoint:

```python
watcher = PortainerImageWatcher(
    portainer,
    endpoint_id=1,
    interval=timedelta(hours=12),
)
```

## Configuration

| Parameter     | Type          | Default  | Description                                       |
| ------------- | ------------- | -------- | ------------------------------------------------- |
| `portainer`   | `Portainer`   | —        | The Portainer client instance                     |
| `endpoint_id` | `int \| None` | `None`   | Endpoint to monitor. `None` watches all endpoints |
| `interval`    | `timedelta`   | 12 hours | How often to poll for updates                     |
| `debug`       | `bool`        | `False`  | Enable debug-level logging                        |

## Results

`watcher.results` returns a copy of the current results as a dictionary:

```
dict[(endpoint_id, container_id), PortainerImageWatcherResult]
```

Each `PortainerImageWatcherResult` contains:

| Field          | Type                                 | Description                           |
| -------------- | ------------------------------------ | ------------------------------------- |
| `endpoint_id`  | `int \| None`                        | The endpoint the container belongs to |
| `container_id` | `str \| None`                        | The container ID                      |
| `status`       | `PortainerImageUpdateStatus \| None` | The image update check result         |

`PortainerImageUpdateStatus` fields:

| Field              | Type          | Description                                          |
| ------------------ | ------------- | ---------------------------------------------------- |
| `update_available` | `bool`        | `True` if a newer image is available in the registry |
| `local_digest`     | `str \| None` | Digest of the locally running image                  |
| `registry_digest`  | `str \| None` | Digest of the latest image in the registry           |

## Runtime control

### Changing the interval

The polling interval can be updated at any time. The new value takes effect after the next completed check:

```python
from datetime import timedelta

watcher.interval = timedelta(hours=1)
```

It is however recommended to not thunderherd the registry with too frequent checks, especially if you have many containers or endpoints. A reasonable interval is usually between 6 and 24 hours, depending on how often you update your images.
Registries may rate-limit requests, so adjust accordingly if you have many containers or a registry with strict limits.

### Checking when the last poll ran

```python
import datetime

if watcher.last_check:
    last = datetime.datetime.fromtimestamp(watcher.last_check)
    print(f"Last checked at: {last}")
```

### Stopping the watcher

```python
watcher.stop()
```

Calling `stop()` cancels the background task. Call `start()` again to restart it.

## API reference

::: pyportainer.watcher
