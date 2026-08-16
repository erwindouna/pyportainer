# Event Listener

`pyportainer` includes a built-in `PortainerEventListener` that maintains a streaming connection to the Docker events endpoint. Unlike the image watcher, which polls on a fixed interval, the event listener reacts in real time as events occur; container starts, stops, crashes, image pulls, network changes, and more.

## How it works

1. On `start()`, a background asyncio task is created.
2. The task resolves which endpoints to listen to (all, or a specific one). If no `endpoint_id` was given, `get_endpoints()` is called to discover them; on a timeout or connection error this retries indefinitely, waiting `reconnect_interval` between attempts, so a Portainer instance that isn't reachable yet at startup doesn't prevent the listener from eventually coming up.
3. One persistent HTTP streaming connection is opened per endpoint, concurrently, via `asyncio.gather`.
4. Each incoming Docker event is parsed and delivered to registered callbacks immediately.
5. If a connection drops (network error, server restart) or a malformed event is received, it is automatically re-established after `reconnect_interval`. See [Error handling](#error-handling) for exactly which errors trigger a reconnect.
6. Authentication errors are treated as fatal for that endpoint — no retry is attempted.
7. Endpoints are isolated from one another: each runs its own reconnect loop, so one endpoint hitting a fatal error (e.g. bad credentials) does not stop streaming from the others. If a per-endpoint task terminates unexpectedly, it is logged with a full traceback rather than propagating out of `start()`.

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
listener.stop()  # Cancels all streaming connections
listener.start()  # Reconnects and starts listening again
```

### Changing the reconnect interval

```python
from datetime import timedelta

listener._reconnect_interval = timedelta(seconds=30)
```

## Error handling

All errors raised while streaming are subclasses of `PortainerError` (see `pyportainer.exceptions`):

| Exception                       | Raised when                                                                  |
| -------------------------------- | ----------------------------------------------------------------------------- |
| `PortainerAuthenticationError`   | The API key is rejected (HTTP 401), either when opening the stream or when discovering endpoints |
| `PortainerTimeoutError`          | The connection cannot be established, or the request times out, within the configured request timeout |
| `PortainerConnectionError`       | The connection is lost mid-stream, or a network error occurs (DNS failure, reset connection, etc.) |
| `PortainerError`                 | A generic streaming failure — currently only raised when a line from the event stream fails to parse as JSON |

### Inside `PortainerEventListener`

`PortainerEventListener` catches these internally so a caller normally never sees them; how each is handled depends on the exception:

- **`PortainerAuthenticationError`** is fatal for the affected endpoint. It is logged with `_LOGGER.exception` (full traceback) and that endpoint's listen loop returns — it will not be retried. Other endpoints keep running unaffected.
- **`PortainerTimeoutError`** and **`PortainerConnectionError`** are treated as transient. A warning is logged including the error message, then the loop waits `reconnect_interval` before reopening the stream.
- **Any other `PortainerError`** (for example, a malformed JSON event line) is also treated as transient: it is logged with a full traceback and the connection is retried after `reconnect_interval`.
- The same timeout/connection-error handling applies to endpoint discovery in `_resolve_endpoint_ids` when `endpoint_id` is `None` — see [How it works](#how-it-works).
- Exceptions that aren't `PortainerError` subclasses (unexpected bugs, cancellation aside) are not caught by the reconnect loop. They propagate out of that endpoint's task, are collected by `asyncio.gather(..., return_exceptions=True)`, and logged as an error with a traceback — they do not crash the other endpoints' listeners or `start()` itself.

None of this requires any handling on your part when using `PortainerEventListener` — it's documented here so you know what to expect in the logs, and can tune `reconnect_interval` accordingly.

### Calling `get_events` / `get_recent_events` directly

Unlike `PortainerEventListener`, the raw `get_events` and `get_recent_events` methods do **not** catch or retry on these errors — they propagate to the caller, since there's no reconnect policy to apply on your behalf. Wrap them yourself if you need resilience:

```python
from pyportainer.exceptions import PortainerAuthenticationError, PortainerConnectionError, PortainerError, PortainerTimeoutError

try:
    async for event in portainer.get_events(endpoint_id=1):
        print(event.type, event.action)
except PortainerAuthenticationError:
    print("Invalid API key")
except (PortainerTimeoutError, PortainerConnectionError) as err:
    print(f"Stream interrupted, consider reconnecting: {err}")
except PortainerError as err:
    print(f"Streaming error: {err}")
```

A `PortainerError` here most commonly means a single event line could not be parsed as JSON; the stream is not resumable after this — reopen it by calling `get_events` again if you want to keep listening.

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
