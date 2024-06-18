"""Tests for regions."""

from spothinta_api.const import REGION_TO_TIMEZONE, Region


async def test_each_region_has_a_time_zone() -> None:
    """Tests that each region has a time zone set."""
    for region in Region:
        assert isinstance(REGION_TO_TIMEZONE[region], str)
