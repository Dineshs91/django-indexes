import re
import json

import sqlparse
from django.db import connection
from django.conf import settings
from rest_framework.response import Response


class IndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.DEBUG:
            return response

        sql_queries = self.gather_sql_queries()
        self.analyze_sql_queries(sql_queries)

        if isinstance(response, Response) and hasattr(response, "data"):
            try:
                response.data["metrics"] = {
                    "indexes": "sample index"
                }
                response.content = json.dumps(response.data)
            except TypeError:
                return response

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

                print(filter_columns)

    @staticmethod
    def _get_table_name(tokens):
        for index, token in enumerate(tokens):
            if token.startswith("FROM"):
                return tokens[index+1]

    @staticmethod
    def _get_columns(filter_clause, table_name):
        print(filter_clause, table_name)
        m = re.findall(r"{}\.[a-zA-Z_]+".format(table_name), filter_clause)

        return m
