"""Asynchronous example for the dev server."""

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
