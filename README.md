# Django Simple Analytics

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
- User: The user who performed the request. If the user is not authenticated, it will show as AnonymousUser.
- view\_count: The number of requests to that page, per date and per method used.

## Licence

This package is distributed under [MIT Licence](./LICENCE).
