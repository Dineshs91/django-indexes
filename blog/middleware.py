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

    @staticmethod
    def analyze_sql_queries(sql_queries):
        for sql_query in sql_queries:
            parsed = sqlparse.parse(sql_query)
            stmt = parsed[0]

            end_clause = stmt.tokens[-1]
            if end_clause.startswith(".WHERE"):
                table_name = ""

    @staticmethod
    def _is_select_statement(sql_query):
        pass

    @staticmethod
    def _get_table_name(sql_query):
        pass
