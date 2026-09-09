# -*- coding: utf-8 -*-
import re
from pathlib import Path

from setuptools import find_packages, setup

# The version is READ, not imported.
#
# `from whitelabel import __version__` runs `whitelabel/__init__.py`, which
# imports frappe — and setup.py is executed by the build backend in an isolated
# environment where frappe does not exist and cannot. Every editable install
# therefore died with `ModuleNotFoundError: No module named 'frappe'` before it
# had installed anything:
#
#     uv pip install -e apps/whitelabel
#     ... File "whitelabel/__init__.py", line 3, in <module>
#         import frappe
#     ModuleNotFoundError: No module named 'frappe'
#
# Worse than the failure itself is what it leaves behind: `bench get-app` has
# already written the app's name into `sites/apps.txt` by this point and does
# not take it back out, and frappe imports every app listed there before running
# ANY bench command. So one failed install puts a traceback in front of every
# command on that bench, and `bench backup` reports it as "Database or
# site_config.json may be corrupted" — which it is not.
version = re.search(
	r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]',
	(Path(__file__).parent / "whitelabel" / "__init__.py").read_text(encoding="utf-8"),
	re.MULTILINE,
).group(1)

setup(
	name="whitelabel",
	version=version,
	description="ERPNext Whitelabel",
	author="Bhavesh Maheshwari",
	author_email="maheshwaribhavesh95863@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	# frappe is deliberately NOT declared. It is supplied by the bench this app
	# is installed into, and listing it sends the resolver to PyPI for an
	# unrelated package of the same name.
	install_requires=[],
)
