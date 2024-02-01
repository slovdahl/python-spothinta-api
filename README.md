# Spot-Hinta.fi Python client

Asynchronous Python client for the [spot-hinta.fi][spothinta] API.

[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]

[![Build Status][build-shield]][build-url]
[![Typing Status][typing-shield]][typing-url]

## About

A Python package with which you can retrieve the energy market prices from [spot-hinta.fi][spothinta].

Based on the [easyEnergy][easyenergy] library by [@klaasnicolaas][klaasnicolaas].

## Installation

```bash
pip install spothinta-api
```

## Data

This client currently supports getting today's and tomorrow's  hourly energy prices. The prices for tomorrow are usually published between 14:00 and 15:00. See [spot-hinta.fi API documentation][spothinta-api-docs] for more information about the available data.

## Example

```python
import asyncio

from datetime import date
from spothinta import SpotHinta


async def main() -> None:
    """Show example on fetching the energy prices from spot-hinta.fi."""
    async with SpotHinta() as client:
        energy = await client.energy_prices()


if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.10+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## License

MIT License

Copyright (c) 2022-2023 Sebastian Lövdahl, Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<!-- MARKDOWN LINKS & IMAGES -->
[easyenergy]: https://github.com/klaasnicolaas/python-easyenergy
[spothinta]: https://spot-hinta.fi/
[spothinta-api-docs]: https://api.spot-hinta.fi/swagger/ui#/(JSON)%20Price%20today%20and%20tomorrow%20(if%20tomorrow%20prices%20exist)/TodayAndDayForward
[klaasnicolaas]: https://github.com/klaasnicolaas

[build-shield]: https://github.com/slovdahl/python-spothinta/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/slovdahl/python-spothinta/actions/workflows/tests.yaml
[code-quality-shield]: https://github.com/slovdahl/python-spothinta/actions/workflows/codeql.yaml/badge.svg
[code-quality]: https://github.com/slovdahl/python-spothinta/actions/workflows/codeql.yaml
[codecov-shield]: https://codecov.io/gh/slovdahl/python-spothinta/branch/main/graph/badge.svg?token=RYhiDUamT6
[codecov-url]: https://codecov.io/gh/slovdahl/python-spothinta
[maintainability-shield]: https://api.codeclimate.com/v1/badges/8628757a4bde52dbfaf6/maintainability
[maintainability-url]: https://codeclimate.com/github/slovdahl/python-spothinta/maintainability
[pypi]: https://pypi.org/project/easyenergy/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/easyenergy
[typing-shield]: https://github.com/slovdahl/python-spothinta/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/slovdahl/python-spothinta/actions/workflows/typing.yaml
[releases-shield]: https://img.shields.io/github/release/slovdahl/python-spothinta.svg
[releases]: https://github.com/slovdahl/python-spothinta/releases

[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
