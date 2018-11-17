import os
import re
import json

import redis
import sqlparse
from django.db import connection
from django.conf import settings
from rest_framework.response import Response

from utils.common import IndexConstraints


class IndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        self.r = redis.Redis(host=redis_host, port=6379, db=0)

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.DEBUG:
            return response

        sql_queries = self.gather_sql_queries()
        self.analyze_sql_queries(sql_queries)

        return response

    @staticmethod
    def gather_sql_queries():
        sql_queries = []
        for index, query in enumerate(connection.queries):
            sql_query = str(query["sql"])
            sql_query = sql_query.replace("\"", "")

            sql_queries.append(sql_query)

        return sql_queries

    def analyze_sql_queries(self, sql_queries):
        for sql_query in sql_queries:
            parsed = sqlparse.parse(sql_query)
            stmt = parsed[0]

            tokens = []

            # Strip whitespaces from tokens.
            for token in stmt.tokens:
                if str(token) == " ":
                    continue
                else:
                    tokens.append(str(token))

            start_clause = tokens[0]
            end_clause = tokens[-1]

            if not start_clause.startswith("SELECT"):
                continue

            if end_clause.startswith("WHERE"):
                table_name = self._get_table_name(tokens)
                filter_columns = self._get_columns(end_clause, table_name)

                valid_columns = self._get_valid_columns_for_index(table_name, filter_columns)

                key = sql_query

                value = self.r.get(key)
                if value is None:
                    self.r.lpush("indexes", key)
                    self.r.set(key, json.dumps({
                        "table": table_name,
                        "columns": valid_columns,
                        "count": 1
                    }))
                else:
                    value = json.loads(value)
                    self.r.set(key, json.dumps({
                        "table": value.get("table"),
                        "columns": value.get("columns"),
                        "count": value.get("count") + 1
                    }))

    @staticmethod
    def _get_valid_columns_for_index(table, columns):
        valid_columns = []
        for column in columns:
            if IndexConstraints().is_valid_index(table, column):
                valid_columns.append(column)

        return valid_columns

    @staticmethod
    def _get_table_name(tokens):
        for index, token in enumerate(tokens):
            if token.startswith("FROM"):
                return tokens[index+1]

    @staticmethod
    def _get_columns(filter_clause, table_name):
        m = re.findall(r"{}\.([a-zA-Z_]+)".format(table_name), filter_clause)

        return m
