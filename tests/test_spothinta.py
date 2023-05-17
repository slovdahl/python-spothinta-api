"""Basic tests for the spot-hinta.fi API."""
# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aresponses import Response, ResponsesMockServer

from spothinta import SpotHinta
from spothinta.exceptions import SpotHintaConnectionError, SpotHintaError

from . import load_fixtures


async def test_json_request(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
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
        response = await client._request()
        assert response is not None
        await client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test internal session is handled correctly."""
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
    async with SpotHinta() as client:
        await client._request()


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout is handled correctly."""
    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(body="Goodmorning!")

    aresponses.add("api.spot-hinta.fi", "/TodayAndDayForward", "GET", response_handler)

    async with ClientSession() as session:
        client = SpotHinta(session=session, request_timeout=0.1)
        with pytest.raises(SpotHintaConnectionError):
            assert await client._request()


async def test_content_type(aresponses: ResponsesMockServer) -> None:
    """Test request content type error is handled correctly."""
    aresponses.add(
        "api.spot-hinta.fi",
        "/TodayAndDayForward",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )

    async with ClientSession() as session:
        client = SpotHinta(
            session=session,
        )
        with pytest.raises(SpotHintaError):
            assert await client._request()


async def test_client_error() -> None:
    """Test request client error is handled correctly."""
    async with ClientSession() as session:
        client = SpotHinta(session=session)
        with patch.object(
            session,
            "request",
            side_effect=ClientError,
        ), pytest.raises(SpotHintaConnectionError):
            assert await client._request()
