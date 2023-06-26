"""Data models for the spot-hinta.fi API."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


def _timed_value(moment: datetime, prices: dict[datetime, float]) -> float | None:
    """Return a function that returns a value at a specific time.

    Args:
    ----
        moment: The time to get the value for.
        prices: A dictionary with market prices.

    Returns:
    -------
        The value at the specific time.
    """
    value = None
    for timestamp, price in prices.items():
        future_dt = timestamp + timedelta(hours=1)
        if timestamp <= moment < future_dt:
            value = round(price, 5)
    return value


def _get_pricetime(
    prices: dict[datetime, float],
    func: Callable[[dict[datetime, float]], datetime],
) -> datetime | None:
    """Return the time of the price.

    Args:
    ----
        prices: A dictionary with market prices.
        func: A function to get the time.

    Returns:
    -------
        The time of the price or None if prices is None or empty.
    """
    if prices is None or len(prices) == 0:
        return None

    return func(prices, key=prices.get)  # type: ignore[call-arg]


@dataclass
class Electricity:
    """Object representing electricity data."""

    prices: dict[datetime, float]

    @property
    def current_price(self) -> float | None:
        """Return the price for the current hour.

        Returns
        -------
            The price for the current hour or None if no price is available.
        """
        return self.price_at_time(self.utcnow())

    @property
    def lowest_price_today(self) -> float | None:
        """Return the minimum price today.

        Returns
        -------
            The minimum price today or None if no prices are available for today.
        """
        prices = self.prices_today()

        if len(prices) == 0:
            return None

        return round(min(prices.values()), 5)

    @property
    def highest_price_today(self) -> float | None:
        """Return the maximum price today.

        Returns
        -------
            The maximum price today or None if no prices are available for today.
        """
        prices = self.prices_today()

        if len(prices) == 0:
            return None

        return round(max(prices.values()), 5)

    @property
    def average_price_today(self) -> float | None:
        """Return the average price today.

        Returns
        -------
            The average price today or None if no prices are available for today.
        """
        prices_today = self.prices_today()

        if len(prices_today) == 0:
            return None

        return round(sum(prices_today.values()) / len(prices_today), 5)

    @property
    def highest_price_time_today(self) -> datetime | None:
        """Return the time of the highest price today.

        Returns
        -------
            The time of the highest price or None if no prices are available for today.
        """
        return _get_pricetime(self.prices_today(), max)

    @property
    def lowest_price_time_today(self) -> datetime | None:
        """Return the time of the lowest price today.

        Returns
        -------
            The time of the lowest price or None if no prices are available for today.
        """
        return _get_pricetime(self.prices_today(), min)

    @property
    def timestamp_prices(self) -> list[dict[str, float | datetime]]:
        """Return a dictionary with the prices.

        Returns
        -------
            A dictionary with the prices.
        """
        return self.generate_timestamp_list(self.prices_today())

    @property
    def hours_priced_equal_or_lower(self) -> int:
        """Return the number of hours with the current price or better.

        Returns
        -------
            The number of hours with the current price or better.
        """
        current = self.current_price or 0
        return sum(price <= current for price in self.prices_today().values())

    def prices_today(self) -> dict[datetime, float]:
        """Return the prices for today.

        Returns
        -------
            The prices for today.
        """
        prices_today = {}
        today = datetime.utcnow().astimezone().date()  # noqa: DTZ003
        for timestamp, price in self.prices.items():
            if timestamp.date() == today:
                prices_today[timestamp] = price
        return prices_today

    def utcnow(self) -> datetime:
        """Return the current timestamp in the UTC timezone.

        Returns
        -------
            The current timestamp in the UTC timezone.
        """
        return datetime.now(timezone.utc)

    def generate_timestamp_list(
        self,
        prices: dict[datetime, float],
    ) -> list[dict[str, float | datetime]]:
        """Return a list of dictionaries with the prices and timestamps.

        Args:
        ----
            prices: A dictionary with the prices.

        Returns:
        -------
            A list of dictionaries with the prices and timestamps.
        """
        timestamp_prices: list[dict[str, float | datetime]] = []
        for timestamp, price in prices.items():
            timestamp_prices.append({"timestamp": timestamp, "price": round(price, 5)})
        return timestamp_prices

    def price_at_time(self, moment: datetime) -> float | None:
        """Return the price at a specific time.

        Args:
        ----
            moment: The time to get the price for.
            data_type: The type of data to get the price for.
                Can be "usage" (default) or "return".

        Returns:
        -------
            The price at the specified time.
        """
        # Get the price at the specified time
        value = _timed_value(moment, self.prices)
        if value is not None or value == 0:
            return value
        return None

    @classmethod
    def from_dict(cls: type[Electricity], data: list[dict[str, Any]]) -> Electricity:
        """Create an Electricity object from a dictionary.

        Args:
        ----
            data: A dictionary with the data from the API.

        Returns:
        -------
            An Electricity object.
        """
        prices: dict[datetime, float] = {}
        for item in data:
            prices[datetime.strptime(item["DateTime"], "%Y-%m-%dT%H:%M:%S%z")] = item[
                "PriceWithTax"
            ]
        return cls(
            prices=prices,
        )
