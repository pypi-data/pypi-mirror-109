#!/usr/bin/env python3
#
#  rsc_on_this_day.py
"""
Displays Royal Society of Chemistry "On This Day In Chemistry" facts in your terminal.
"""
#
#  Copyright © 2019-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Cached copies of the RSC On This Day website Copyright © 2020 Royal Society of Chemistry
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import datetime
from typing import Tuple, Union

# 3rd party
import click
from apeye.cache import Cache
from apeye.requests_url import RequestsURL
from bs4 import BeautifulSoup  # type: ignore
from domdf_python_tools.dates import check_date, months, parse_month

__author__ = "Dominic Davis-Foster"
__copyright__ = "2019-2021 Dominic Davis-Foster"
__license__ = "MIT"
__version__ = "0.3.0"
__email__ = "dominic@davis-foster.co.uk"

__all__ = ["clear_cache", "get_fact", "fact_cache"]

# TODO: Timeout

fact_cache = Cache("rsc_on_this_day")

_base_url = RequestsURL(
		"https://web.archive.org/web/20190331053029id_/"
		"http://www.rsc.org/learn-chemistry/collections/chemistry-calendar/"
		)

date_arg_error_str = "If requesting a specific date both the month and day must be given."

month_full_names = list(months.values())
month_short_names = list(months.keys())


@fact_cache
def get_fact(
		month: Union[str, int, None] = None,
		day: Union[str, int, None] = None,
		) -> Tuple[str, str]:
	"""
	Returns the fact for the given date.

	:param month: The month, either its short name (e.g. ``'Oct'``), its full name (e.g. ``'October'``)
		or its number (e.g. ``10``).
	:param day: The day of the month.

	If ``month`` and ``day`` are both left as :py:obj:`None` (the default) the current date is used.
	"""

	if (month and day is None) or (day and month is None):
		raise SyntaxError(date_arg_error_str)

	if month is None and day is None:
		today = datetime.date.today()

		month = today.strftime("%B")
		day = today.day

	if month is None or day is None:
		raise SyntaxError(date_arg_error_str)

	month = parse_month(month)

	# Check that the date is valid
	if not check_date(month, day):  # type: ignore
		raise ValueError(f"Invalid day {day!r} for month {month!r}")

	page = (_base_url / f"{month}-{day}").get()
	soup = BeautifulSoup(page.content, "html.parser")

	header = soup.find("div", {"class": "description"}).previousSibling.previousSibling.get_text().strip()
	body = soup.find("div", {"class": "description"}).get_text().strip()

	return header, body


def clear_cache() -> int:
	"""
	Clear any cached responses.
	"""

	if fact_cache.clear():
		click.echo("Cache cleared successfully.")
		return 0

	return 1
