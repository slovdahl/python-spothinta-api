"""Asynchronous Python client for the spot-hinta.fi API."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, cast

import async_timeout
from aiohttp.client import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .const import API_HOST
from .exceptions import (
    SpotHintaConnectionError,
    SpotHintaError,
    SpotHintaNoDataError,
)
from .models import Electricity


@dataclass
class SpotHinta:
    """Main class for handling data fetching from spot-hinta.fi."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        *,
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
            SpotHintaConnectionError: An error occurred while
                communicating with the API.
            SpotHintaError: Received an unexpected response from
                the API.
        """
        version = metadata.version(__package__)

        url = URL.build(
            scheme="https",
            host=API_HOST,
            path="/TodayAndDayForward",
        )

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonSpotHinta/{version}",
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
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the API."
            raise SpotHintaConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with the API."
            raise SpotHintaConnectionError(
                msg,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the spot-hinta.fi API"
            raise SpotHintaError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def energy_prices(self) -> Electricity:
        """Get energy prices for a given period.

        Returns
        -------
            A Python dictionary with the response from spot-hinta.fi.

        Raises
        ------
            SpotHintaNoDataError: No energy prices found for this period.
        """
        data = await self._request()

        if len(data) == 0:
            msg = "No energy prices found for this period."
            raise SpotHintaNoDataError(msg)
        return Electricity.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> SpotHinta:
        """Async enter.

        Returns
        -------
            The SpotHinta object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
