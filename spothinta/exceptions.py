"""Exceptions for spot-hinta.fi."""


class SpotHintaError(Exception):
    """Generic spot-hinta.fi exception."""


class SpotHintaConnectionError(SpotHintaError):
    """spot-hinta.fi - connection exception."""


class SpotHintaNoDataError(SpotHintaError):
    """spot-hinta.fi - no data exception."""
