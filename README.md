# django-indexes

This package suggests indexes that can be added, by analysing the queries by intercepting requests.

By default django adds indexes for primary fields, foreign fields and if a field is unique.
Also the package ignores boolean fields, as this field has a cardinality of 2 (True/False). So
improvement can be gained by adding an index on such fields.

*Cardinality refers to the uniqueness of data values contained in a column*

Low cardinality example: pincode, city
High cardinality example: email, address, phonenumber 

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

This will work only with `APIClient`

## Support

Currently this package supports Django>2.0. But with some small changes can be made to support older
versions as well.

## Demo

`docker-compose up -d`

Make some requests from postman, by creating the blog and its posts.
