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
import sys
import textwrap
from typing import Union

# 3rd party
import click
from consolekit import click_command
from consolekit.options import auto_default_argument, auto_default_option, flag_option

# this package
import rsc_on_this_day

__all__ = ["main"]


def clear_cache_callback(context: click.Context, param: click.Parameter, value):
	if value:
		sys.exit(rsc_on_this_day.clear_cache())


@auto_default_argument("day", type=click.INT)
@auto_default_argument("month", type=click.STRING)
@auto_default_option(
		"-w",
		"--width",
		type=click.INT,
		show_default=True,
		help="The number of characters per line of the output. Set to -1 to disable wrapping."
		)
@flag_option(
		"--clear-cache",
		help="Clear any cached data and exit.",
		callback=clear_cache_callback,
		expose_value=False,
		is_eager=True,
		)
@click.version_option(rsc_on_this_day.__version__)
@click_command()
def main(
		month: Union[str, int, None] = None,
		day: Union[str, int, None] = None,
		width: int = 80,
		):
	"""
	Display the Royal Society of Chemistry "On This Day In Chemistry" fact for the given day.

	If no date is given the current date is used.
	"""

	try:
		header, body = rsc_on_this_day.get_fact(month, day)
	except (SyntaxError, ValueError) as e:
		raise click.UsageError(str(e))

	if width > 0:
		header = textwrap.fill(header, width)
		body = textwrap.fill(body, width)

	# print(f"{day}/{month}")
	print(header)
	print(body)


if __name__ == "__main__":
	sys.exit(main())
