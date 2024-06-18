"""Constants for SpotHinta API client."""

from __future__ import annotations

from enum import Enum, unique
from typing import Final

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


REGION_TO_TIMEZONE: dict[Region, str] = {
    Region.DK1: "Europe/Copenhagen",
    Region.DK2: "Europe/Copenhagen",
    Region.FI: "Europe/Helsinki",
    Region.EE: "Europe/Tallinn",
    Region.LT: "Europe/Vilnius",
    Region.LV: "Europe/Riga",
    Region.NO1: "Europe/Oslo",
    Region.NO2: "Europe/Oslo",
    Region.NO3: "Europe/Oslo",
    Region.NO4: "Europe/Oslo",
    Region.NO5: "Europe/Oslo",
    Region.SE1: "Europe/Stockholm",
    Region.SE2: "Europe/Stockholm",
    Region.SE3: "Europe/Stockholm",
    Region.SE4: "Europe/Stockholm",
}
