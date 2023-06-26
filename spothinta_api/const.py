"""Constants for SpotHinta API client."""
from enum import Enum, unique
from typing import Final
from zoneinfo import ZoneInfo

API_HOST: Final = "api.spot-hinta.fi"


@unique
class Region(Enum):
    """An enumeration of the supported regions."""

    DK1 = 0
    DK2 = 1
    FI = 2
    EE = 3
    LT = 4
    LV = 5
    NO1 = 6
    NO2 = 7
    NO3 = 8
    NO4 = 9
    NO5 = 10
    SE1 = 11
    SE2 = 12
    SE3 = 13
    SE4 = 14


REGION_TO_TIMEZONE: dict[Region, ZoneInfo] = {
    Region.DK1: ZoneInfo("Europe/Copenhagen"),
    Region.DK2: ZoneInfo("Europe/Copenhagen"),
    Region.FI: ZoneInfo("Europe/Helsinki"),
    Region.EE: ZoneInfo("Europe/Tallinn"),
    Region.LT: ZoneInfo("Europe/Vilnius"),
    Region.LV: ZoneInfo("Europe/Riga"),
    Region.NO1: ZoneInfo("Europe/Oslo"),
    Region.NO2: ZoneInfo("Europe/Oslo"),
    Region.NO3: ZoneInfo("Europe/Oslo"),
    Region.NO4: ZoneInfo("Europe/Oslo"),
    Region.NO5: ZoneInfo("Europe/Oslo"),
    Region.SE1: ZoneInfo("Europe/Stockholm"),
    Region.SE2: ZoneInfo("Europe/Stockholm"),
    Region.SE3: ZoneInfo("Europe/Stockholm"),
    Region.SE4: ZoneInfo("Europe/Stockholm"),
}
