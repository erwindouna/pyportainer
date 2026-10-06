"""Progress tracking for Docker image pulls."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyportainer.models.image_pull import DockerImagePullEvent

# Share of a layer's progress taken by the download, the rest is extraction
DOWNLOAD_SHARE = 0.8

_LAYER_START = {"Pulling fs layer", "Waiting"}
_LAYER_DOWNLOADED = {"Verifying Checksum", "Download complete"}
_LAYER_DONE = {"Pull complete", "Already exists"}


class ImagePullProgress:
    """Turn Docker image pull events into an overall percentage.

    Docker announces every layer before the first download starts, but a
    layer's size is only known once its own download starts. Each layer
    therefore counts equally, the percentage stays 0 until a download starts
    and it never goes down.
    """

    def __init__(self) -> None:
        """Initialize the progress tracker."""
        self._layers: dict[str, float] = {}
        self._started = False
        self._percentage = 0.0

    @property
    def percentage(self) -> float:
        """Return the overall progress of the pull, from 0 to 100."""
        return self._percentage

    def update(self, event: DockerImagePullEvent) -> float:
        """Process a pull event and return the overall percentage."""
        if event.id is None or (fraction := _layer_fraction(event)) is None:
            return self._percentage

        self._layers[event.id] = max(fraction, self._layers.get(event.id, 0.0))
        self._started = self._started or event.status not in _LAYER_START | {"Already exists"}
        if not self._started:
            return self._percentage

        self._percentage = max(
            self._percentage,
            sum(self._layers.values()) / len(self._layers) * 100,
        )
        return self._percentage


def _layer_fraction(event: DockerImagePullEvent) -> float | None:
    """Return how far a layer is, or None if the event isn't about a layer."""
    status = event.status
    if status in _LAYER_START:
        return 0.0
    if status in _LAYER_DOWNLOADED:
        return DOWNLOAD_SHARE
    if status in _LAYER_DONE:
        return 1.0

    detail = event.progress_detail
    ratio = detail.current / detail.total if detail and detail.current is not None and detail.total else 0.0
    ratio = min(ratio, 1.0)
    if status == "Downloading":
        return DOWNLOAD_SHARE * ratio
    if status == "Extracting":
        return DOWNLOAD_SHARE + (1 - DOWNLOAD_SHARE) * ratio
    return None
