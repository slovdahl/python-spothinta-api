"""Constants for SpotHinta API client."""
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
