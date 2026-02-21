# Event Listener

`pyportainer` includes a built-in `PortainerEventListener` that maintains a streaming connection to the Docker events endpoint. Unlike the image watcher, which polls on a fixed interval, the event listener reacts in real time as events occur; container starts, stops, crashes, image pulls, network changes, and more.

## How it works

1. On `start()`, a background asyncio task is created.
2. The task resolves which endpoints to listen to (all, or a specific one).
3. One persistent HTTP streaming connection is opened per endpoint, concurrently.
4. Each incoming Docker event is parsed and delivered to registered callbacks immediately.
5. If a connection drops (network error, server restart), it is automatically re-established after `reconnect_interval`.
6. Authentication errors are treated as fatal for that endpoint — no retry is attempted.

## Basic usage

```python
import asyncio
from datetime import timedelta

from pyportainer import Portainer, PortainerEventListener
from pyportainer.listener import PortainerEventListenerResult


async def on_event(result: PortainerEventListenerResult) -> None:
    """Handle an incoming Docker event."""
    print(f"[endpoint {result.endpoint_id}] {result.event.type} {result.event.action}")


async def main() -> None:
    async with Portainer(
        api_url="http://localhost:9000",
        api_key="YOUR_API_KEY",
    ) as portainer:
        listener = PortainerEventListener(portainer)
        listener.register_callback(on_event)
        listener.start()

        await asyncio.sleep(60)  # Listen for a while

        listener.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

## Listening to a specific endpoint

Pass `endpoint_id` to open a stream to a single Portainer endpoint instead of all:

```python
listener = PortainerEventListener(portainer, endpoint_id=1)
```

## Filtering by event type

Use `event_types` to receive only the Docker event categories you care about. Accepted values match the Docker API's `type` filter: `container`, `image`, `volume`, `network`, `daemon`, `plugin`, `node`, `service`, `secret`, `config`.

```python
listener = PortainerEventListener(
    portainer,
    event_types=["container", "image"],
)
```

## Configuration

| Parameter            | Type                | Default   | Description                                                     |
| -------------------- | ------------------- | --------- | --------------------------------------------------------------- |
| `portainer`          | `Portainer`         | —         | The Portainer client instance                                   |
| `endpoint_id`        | `int \| None`       | `None`    | Endpoint to listen to. `None` listens to all endpoints          |
| `event_types`        | `list[str] \| None` | `None`    | Docker event types to filter on. `None` means all types         |
| `reconnect_interval` | `timedelta`         | 5 seconds | How long to wait before reconnecting after a dropped connection |
| `debug`              | `bool`              | `False`   | Enable debug-level logging                                      |

## Event data

Each callback receives a `PortainerEventListenerResult`:

| Field         | Type          | Description                      |
| ------------- | ------------- | -------------------------------- |
| `endpoint_id` | `int`         | The endpoint the event came from |
| `event`       | `DockerEvent` | The Docker event payload         |

`DockerEvent` fields:

| Field       | Type                       | Description                                 |
| ----------- | -------------------------- | ------------------------------------------- |
| `type`      | `str \| None`              | Event category: `container`, `image`, etc.  |
| `action`    | `str \| None`              | What happened: `start`, `stop`, `die`, etc. |
| `actor`     | `DockerEventActor \| None` | The object the event is about               |
| `scope`     | `str \| None`              | `local` or `swarm`                          |
| `time`      | `int \| None`              | Unix timestamp (seconds)                    |
| `time_nano` | `int \| None`              | Unix timestamp (nanoseconds)                |

`DockerEventActor` fields:

| Field        | Type                     | Description                                       |
| ------------ | ------------------------ | ------------------------------------------------- |
| `id`         | `str \| None`            | ID of the object (container ID, image name, etc.) |
| `attributes` | `dict[str, str] \| None` | Extra metadata (image name, container name, etc.) |

## Callbacks

Register a callback to be invoked for every event received. Both sync and async callables are supported.

### Registering a callback

```python
from pyportainer import PortainerEventListener
from pyportainer.listener import PortainerEventListenerResult


def on_event(result: PortainerEventListenerResult) -> None:
    print(f"{result.event.type} {result.event.action} — {result.event.actor.id}")


listener = PortainerEventListener(portainer, endpoint_id=1)
listener.register_callback(on_event)
listener.start()
```

### Async callbacks

```python
async def on_event(result: PortainerEventListenerResult) -> None:
    if result.event.action == "die":
        await alert(f"Container {result.event.actor.id} has stopped unexpectedly")


listener.register_callback(on_event)
```

### Filtering inside a callback

Callbacks receive every event that passes the `event_types` filter. Add further logic inside the callback:

```python
def on_event(result: PortainerEventListenerResult) -> None:
    if result.event.action not in ("start", "die"):
        return
    print(f"Container {result.event.actor.id}: {result.event.action}")
```

### Unregistering a callback

```python
listener.unregister_callback(on_event)
```

### Notes

- Registering the same callable twice is silently ignored; it is only called once per event.
- Exceptions raised inside a callback are logged but do not stop the listener or prevent other callbacks from running.
- The `EventListenerCallback` type alias is exported from `pyportainer` for type annotations: `from pyportainer import EventListenerCallback`.

## Runtime control

### Stopping and restarting

```python
listener.stop()   # Cancels all streaming connections
listener.start()  # Reconnects and starts listening again
```

### Changing the reconnect interval

```python
from datetime import timedelta

listener._reconnect_interval = timedelta(seconds=30)
```

## Querying events directly

The underlying `get_events` and `get_recent_events` methods on the `Portainer` client are also available directly, without using `PortainerEventListener`.

### Stream events in real time

`get_events` is an async generator that keeps the connection open and yields events as they arrive:

```python
async for event in portainer.get_events(endpoint_id=1):
    print(event.type, event.action)
```

Pass `since` to replay events from a specific point, or `until` to close the stream automatically at a timestamp:

```python
from datetime import UTC, datetime, timedelta

async for event in portainer.get_events(
    endpoint_id=1,
    since=datetime.now(UTC) - timedelta(hours=1),
    filters={"type": ["container"], "event": ["start", "die"]},
):
    print(event.action, event.actor.id)
```

### Fetch a bounded list of past events

`get_recent_events` collects all events in a time window into a list and returns once the window is exhausted:

```python
from datetime import UTC, datetime, timedelta

events = await portainer.get_recent_events(
    endpoint_id=1,
    since=datetime.now(UTC) - timedelta(hours=1),
)
for event in events:
    print(event.type, event.action)
```

`until` defaults to now, so the connection closes automatically. You can also pass an explicit end time:

```python
events = await portainer.get_recent_events(
    endpoint_id=1,
    since=datetime(2024, 1, 1, tzinfo=UTC),
    until=datetime(2024, 1, 2, tzinfo=UTC),
    filters={"type": ["image"]},
)
```

## API reference

::: pyportainer.listener
