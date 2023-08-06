# django_datahooks
<!-- start-no-pypi -->
[![codecov](https://codecov.io/gh/labd/django-datahooks/branch/master/graph/badge.svg)](https://codecov.io/gh/labd/django-datahooks)
[![pypi](https://img.shields.io/pypi/v/django-datahooks.svg)](https://pypi.python.org/pypi/django-datahooks/)
[![readthedocs](https://readthedocs.org/projects/django-datahooks/badge/)](https://django-datahooks.readthedocs.io/en/latest/)
<!-- end-no-pypi -->

Note: this package is experimental


## Installation

```shell
pip install django_datahooks
```

## Usage

This module auto detects modules in your django apps at `.datahooks.*` and
scans for classes extending `django_datahooks.DataProvider` to
makes them available for the `manage.py generate_data <provider>` command.


Example:

```python
from django.core.management import call_command
from django_datahooks import DataProvider


class PagesProvider(DataProvider):
    name = "pages"

    def run(self, **options):
        # Run creation commands

```
