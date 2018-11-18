import os
import json

import redis
from rest_framework import status
from rest_framework.views import APIView

from utils.common import create_response


class StatsView(APIView):
    def get(self, request):
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        r = redis.Redis(host=redis_host, port=6379, db=0)

        index_length = r.llen("indexes")
        indexes = r.lrange("indexes", 0, index_length)

        if not indexes:
            return create_response(data=[], status=status.HTTP_200_OK)

        response_data = {
            "indexes": []
        }

        for index in indexes:
            value = r.get(index)
            value = json.loads(value)

            response_data["indexes"].append({
                "sql": value.get("sql"),
                "table": value.get("table"),
                "columns": value.get("columns"),
                "count": value.get("count")
            })

        return create_response(data=response_data, status=status.HTTP_200_OK)
