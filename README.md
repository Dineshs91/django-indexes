# django-indexes

This package suggests indexes that can be added, by analysing the queries by intercepting requests.

By default django adds indexes for primary fields, foreign fields and if a field is unique.
Also the package ignores boolean fields, as this field has a cardinality of 2 (True/False). So
improvement can be gained by adding an index on such fields.

*Cardinality refers to the uniqueness of data values contained in a column*

Low cardinality example: pincode, city
High cardinality example: email, address, phonenumber 

## Install

`python setup.py`

## Demo

`docker-compose up -d`

Make some requests from postman, by creating the blog and its posts.
