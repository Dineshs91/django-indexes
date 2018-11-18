# django-indexes

This package suggests indexes that can be added, by analysing the queries by intercepting requests.

By default django adds indexes for primary fields, foreign fields and if a field is unique.
Also the package ignores boolean fields, as this field has a cardinality of 2 (True/False). So
improvement can be gained by adding an index on such fields.

*Cardinality refers to the uniqueness of data values contained in a column*

Low cardinality example: pincode, city
High cardinality example: email, address, phonenumber 

## Features

- Ignores indexes that django creates by default
  - Primary key
  - Foreign key
  - Unique=True (Unique fields)
- Ignores boolean field as it has very small cardinality.
- Can be run from tests or in a staging server.

## Install

`python setup.py install`

## Usage

This will work only when `DEBUG=True`

Add `django_indexes.middleware.IndexMiddleware` to the middleware in `settings.py`, ideally at the bottom.

You can also add this to your tests.

```python
@override_settings(MIDDLEWARE=[
    'django_indexes.core.middleware.IndexMiddleware'
], DEBUG=True)
def test_user_login(self):
    pass
```

Also make sure redis is running and set the env variable `REDIS_HOST`.

This will work only with `APIClient`

Stats can be checked from `stats.views.StatsView`. You can create an url mapping for this view and
make a GET api call.

## Support

Currently this package supports Django>2.0. But with some small changes can be made to support older
versions as well.

## Demo

`docker-compose up -d`

Make some requests from postman, by creating the blog and its posts. We can also run the tests

```
docker exec -it <api_container> bash
python manage.py test
```

Access this endpoint, after running tests.
```bash
http://localhost:8091/api/stats/
```

![Alt text](https://github.com/dineshs91/django-indexes/blob/master/stats.png?raw=true "Sample screenshot")

## TODO

- [ ] sql joins
- [ ] Nested queries
- [ ] Performance optimizations
