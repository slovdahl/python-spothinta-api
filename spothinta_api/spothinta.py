"""Asynchronous Python client for the spot-hinta.fi API."""

from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import TYPE_CHECKING, Any, cast

import async_timeout
from aiohttp import ClientResponseError
from aiohttp.client import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from aiozoneinfo import async_get_time_zone
from yarl import URL

from .const import API_HOST, REGION_TO_TIMEZONE, Region
from .exceptions import (
    SpotHintaConnectionError,
    SpotHintaError,
    SpotHintaNoDataError,
    SpotHintaRateLimitError,
)
from .models import Electricity

if TYPE_CHECKING:
    from typing_extensions import Self

VERSION = metadata.version(__package__)


@dataclass
class SpotHinta:
    """Main class for handling data fetching from spot-hinta.fi."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the API of spot-hinta.fi.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP method to use, for example, 'GET'
            params: Extra options to improve or limit the response.

        Returns:
        -------
            A Python dictionary (json) with the response from spot-hinta.fi.

        Raises:
        ------
            SpotHintaRateLimitError: If too many requests have been made
                during a given timespan.
            SpotHintaConnectionError: An error occurred while
                communicating with the API.
            SpotHintaError: Received an unexpected response from
                the API.

        """
        url = URL.build(
            scheme="https",
            host=API_HOST,
            path=uri,
        )

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonSpotHinta/{VERSION}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as ex:
            msg = "Timeout occurred while connecting to the API."
            raise SpotHintaConnectionError(
                msg,
            ) from ex
        except (ClientError, socket.gaierror) as ex:
            if isinstance(ex, ClientResponseError) and ex.status == 429:
                msg = "IP address rate limited (HTTP 429)"
                raise SpotHintaRateLimitError(
                    msg,
                ) from ex

            msg = "Error occurred while communicating with the API."
            raise SpotHintaConnectionError(
                msg,
            ) from ex

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the spot-hinta.fi API"
            raise SpotHintaError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def energy_prices(self, region: Region = Region.FI) -> Electricity:
        """Get energy prices for today and tomorrow for a region.

        Args:
        ----
            region: The region to get prices for.

        Returns:
        -------
            A Python dictionary with the response from spot-hinta.fi.

        Raises:
        ------
            SpotHintaNoDataError: No energy prices found.

        """
        data = await self._request(
            uri="/TodayAndDayForward",
            params={"region": region.name},
        )

        if len(data) == 0:
            msg = "No energy prices found."
            raise SpotHintaNoDataError(msg)

        time_zone = await async_get_time_zone(REGION_TO_TIMEZONE[region])
        return Electricity.from_dict(data, time_zone=time_zone)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The SpotHinta object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
