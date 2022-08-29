# Django Simple Analytics

![PyPI](https://img.shields.io/pypi/v/django-simple-analytics?style=for-the-badge)
[![](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
![PyPI - License](https://img.shields.io/pypi/l/django-simple-analytics?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-simple-analytics?style=for-the-badge)

⚠️ This package is still in beta. Do not use for production ⚠️

Simple analytics is a very simple package to track requests done to the website and store them in database.

## Installation

From PYPi using `pip`:

```
pip install django-simple-analytics
```

## Usage

In order to install the package add the following line to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    "simple_analytics",
]
```

This will make the model available for you to call and query. To enable the middleware, add this at the bottom of the middleware list:

```python
MIDDLEWARE = [
    ...
    "simple_analytics.middleware.page_counts",
]
```

Then, you need to run migrations, finally:

```console
./manage.py migrate
```

To actually create the table in the database.

Now every request done to the django website will be recorded in the database with the following fields:

- Date: The date pf the request.
- Page: The path of the request.
- Method: The verb used to request the page.
- Whether the page exists or not.
- Origin: If the header exists in the requst, where the request originated.
- User: The user who performed the request. If the user is not authenticated, it will show as AnonymousUser.
- view_count: The number of requests to that page, per date and per method used.

## Licence

This package is distributed under [MIT Licence](./LICENCE).
