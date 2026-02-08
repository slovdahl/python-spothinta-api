"""Test the models."""

from datetime import datetime, timedelta, timezone

import pytest
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from spothinta_api import (
    Electricity,
    SpotHinta,
    SpotHintaNoDataError,
    SpotHintaUnsupportedResolutionError,
)
from spothinta_api.const import Region

from . import load_fixtures


@pytest.mark.freeze_time("2023-05-06 15:00:00+03:00")
async def test_model(aresponses: ResponsesMockServer) -> None:
    """Test the model for usage at 15:00:00 UTC+3."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices()
        assert energy is not None
        assert isinstance(energy, Electricity)
        assert energy.highest_price_today == 0.1055
        assert energy.highest_price_tomorrow == 0.0972
        assert energy.lowest_price_today == 0.062
        assert energy.lowest_price_tomorrow == 0.0373
        assert energy.average_price_today == 0.08935
        assert energy.average_price_tomorrow == 0.07284
        assert energy.current_price == 0.062
        assert energy.intervals_priced_equal_or_lower == 1
        # The price for another interval
        another_interval = datetime(2023, 5, 6, 17, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_interval) == 0.1055
        assert energy.lowest_price_time_today == datetime.strptime(
            "2023-05-06 15:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.lowest_price_time_tomorrow == datetime.strptime(
            "2023-05-07 16:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_today == datetime.strptime(
            "2023-05-06 20:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_tomorrow == datetime.strptime(
            "2023-05-07 08:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert isinstance(energy.timestamp_prices, list)


@pytest.mark.freeze_time("2025-10-04 15:00:00+03:00")
async def test_model_15_minute_resolution(aresponses: ResponsesMockServer) -> None:
    """Test the model for usage at 15:00:00 UTC+3."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy-15-min.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices(
            resolution=timedelta(minutes=15),
        )
        assert energy is not None
        assert isinstance(energy, Electricity)
        assert energy.highest_price_today == 0.00371
        assert energy.highest_price_tomorrow == 0.00733
        assert energy.lowest_price_today == -0.00001
        assert energy.lowest_price_tomorrow == -0.00004
        assert energy.average_price_today == 0.00131
        assert energy.average_price_tomorrow == 0.00239
        assert energy.current_price == 0.00157
        assert energy.intervals_priced_equal_or_lower == 63
        # The price for another interval
        another_interval = datetime(2025, 10, 4, 17, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_interval) == 0.0033
        assert energy.lowest_price_time_today == datetime.strptime(
            "2025-10-04 5:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.lowest_price_time_tomorrow == datetime.strptime(
            "2025-10-05 4:30:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_today == datetime.strptime(
            "2025-10-04 00:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_tomorrow == datetime.strptime(
            "2025-10-05 20:45:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert isinstance(energy.timestamp_prices, list)


@pytest.mark.freeze_time("2025-10-04 16:00:00+02:00")
async def test_model_se1_15_minute_resolution(aresponses: ResponsesMockServer) -> None:
    """Test the model for usage in region SE1 at 16:00:00 UTC+3."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy-SE1-15-min.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices(
            region=Region.SE1,
            resolution=timedelta(minutes=15),
        )
        assert energy is not None
        assert isinstance(energy, Electricity)
        assert energy.highest_price_today == 0.00289
        assert energy.highest_price_tomorrow == 0.0059
        assert energy.lowest_price_today == 0.00001
        assert energy.lowest_price_tomorrow == 0.00005
        assert energy.average_price_today == 0.00113
        assert energy.average_price_tomorrow == 0.00249
        assert energy.current_price == 0.00128
        assert energy.intervals_priced_equal_or_lower == 57
        # The price for another interval
        another_interval = datetime(2025, 10, 4, 18, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_interval) == 0.00242
        assert energy.lowest_price_time_today == datetime.strptime(
            "2025-10-04 03:00:00+00:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.lowest_price_time_tomorrow == datetime.strptime(
            "2025-10-05 01:15:00+00:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_today == datetime.strptime(
            "2025-10-04 17:30:00+00:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_tomorrow == datetime.strptime(
            "2025-10-05 17:45:00+00:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert isinstance(energy.timestamp_prices, list)


@pytest.mark.freeze_time("2023-05-06 15:00:00+03:00")
async def test_model_no_prices_for_tomorrow(aresponses: ResponsesMockServer) -> None:
    """Test the model for usage at 15:00:00 UTC+3 with no prices for tomorrow."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy-no-tomorrow.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices()
        assert energy is not None
        assert isinstance(energy, Electricity)
        assert energy.highest_price_today == 0.1055
        assert energy.highest_price_tomorrow is None
        assert energy.lowest_price_today == 0.062
        assert energy.lowest_price_tomorrow is None
        assert energy.average_price_today == 0.08935
        assert energy.average_price_tomorrow is None
        assert energy.current_price == 0.062
        assert energy.intervals_priced_equal_or_lower == 1
        # The price for another interval
        another_interval = datetime(2023, 5, 6, 17, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_interval) == 0.1055
        assert energy.lowest_price_time_today == datetime.strptime(
            "2023-05-06 15:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.lowest_price_time_tomorrow is None
        assert energy.highest_price_time_today == datetime.strptime(
            "2023-05-06 20:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time_tomorrow is None
        assert isinstance(energy.timestamp_prices, list)
        assert isinstance(energy.timestamp_prices_today, list)
        assert len(energy.timestamp_prices) == 24
        assert len(energy.timestamp_prices_today) == 24


@pytest.mark.freeze_time("2023-05-06 15:00:00+03:00")
async def test_midnight(aresponses: ResponsesMockServer) -> None:
    """Test the model between 00:00 and 01:00 in UTC+3."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices()
        assert energy is not None
        assert energy.current_price == 0.062


async def test_none_data(aresponses: ResponsesMockServer) -> None:
    """Test when there is no data for the current datetime."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices()
        assert energy is not None
        assert isinstance(energy, Electricity)
        assert energy.current_price is None


@pytest.mark.freeze_time("2023-05-06 19:01:32+03:00")
async def test_only_data_for_tomorrow(aresponses: ResponsesMockServer) -> None:
    """Test when there is only data for tomorrow."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("energy-only-tomorrow.json"),
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        energy: Electricity = await client.energy_prices()
        assert energy is not None
        assert isinstance(energy, Electricity)
        assert energy.current_price is None
        assert energy.average_price_today is None
        assert energy.highest_price_today is None
        assert energy.lowest_price_today is None
        assert energy.intervals_priced_equal_or_lower == 0
        # The price for another interval
        another_interval = datetime(2023, 5, 6, 17, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_interval) is None
        assert energy.lowest_price_time_today is None
        assert energy.highest_price_time_today is None
        assert isinstance(energy.timestamp_prices, list)
        assert isinstance(energy.timestamp_prices_today, list)
        assert len(energy.timestamp_prices) == 24
        assert len(energy.timestamp_prices_today) == 0


async def test_no_electricity_data(aresponses: ResponsesMockServer) -> None:
    """Test when there is no electricity data."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="[]",
        ),
    )
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        with pytest.raises(SpotHintaNoDataError):
            await client.energy_prices()


async def test_unsupported_resolution() -> None:
    """Test an unsupported resolution."""
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        with pytest.raises(SpotHintaUnsupportedResolutionError):
            await client.energy_prices(resolution=timedelta(minutes=45))
