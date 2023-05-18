"""Asynchronous Python client for the spot-hinta.fi API."""

import asyncio
from datetime import timedelta

import pytz

from spothinta import SpotHinta
from spothinta.const import Region


async def main() -> None:
    """Show example on fetching the energy prices from spot-hinta.fi."""
    async with SpotHinta() as client:
        await print_prices(client, Region.FI)
        await print_prices(client, Region.SE2)


async def print_prices(client: SpotHinta, region: Region) -> None:
    """Print prices for the given region."""
    local = pytz.timezone("Europe/Helsinki")

    energy_today = await client.energy_prices(region=region)
    utc_next_hour = energy_today.utcnow() + timedelta(hours=1)
    print(f"--- ENERGY TODAY FOR REGION {region.name}---")
    print(f"Extremas price: {energy_today.extreme_prices}")
    print(f"Average price: {energy_today.average_price}")
    print()

    highest_time = energy_today.highest_price_time.astimezone(local)
    print(f"Highest price time: {highest_time}")
    lowest_time = energy_today.lowest_price_time.astimezone(local)
    print(f"Lowest price time: {lowest_time}")
    print()
    print(f"Current price: {energy_today.current_price}")
    print(f"Next hourprice: {energy_today.price_at_time(utc_next_hour)}")

    lower_hours: int = energy_today.hours_priced_equal_or_lower
    print(f"Lower hours: {lower_hours}")


def start() -> None:
    """Call the main async method."""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
