"""Test the models."""
from datetime import datetime, timezone

import pytest
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from spothinta_api import Electricity, SpotHinta, SpotHintaNoDataError

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
        assert energy.lowest_price_today == 0.062
        assert energy.average_price == 0.08935
        assert energy.current_price == 0.062
        assert energy.hours_priced_equal_or_lower == 1
        # The price for another hour
        another_hour = datetime(2023, 5, 6, 17, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_hour) == 0.1055
        assert energy.lowest_price_time == datetime.strptime(
            "2023-05-06 15:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert energy.highest_price_time == datetime.strptime(
            "2023-05-06 20:00:00+03:00",
            "%Y-%m-%d %H:%M:%S%z",
        )
        assert isinstance(energy.timestamp_prices, list)


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
        assert energy.average_price is None
        assert energy.highest_price_today is None
        assert energy.lowest_price_today is None
        assert energy.hours_priced_equal_or_lower == 0
        # The price for another hour
        another_hour = datetime(2023, 5, 6, 17, 0, tzinfo=timezone.utc)
        assert energy.price_at_time(another_hour) is None
        assert energy.lowest_price_time is None
        assert energy.highest_price_time is None
        assert isinstance(energy.timestamp_prices, list)


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
