from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from rest_framework import status
from rest_framework.response import Response


def create_response(data=None, error=None, status=status.HTTP_200_OK):
    if 200 <= status < 400:
        success = True
    else:
        success = False

    response = {
        'data': data,
        'error': error,
        'success': success
    }
    return Response(data=response, status=status)


class IndexConstraints(object):
    def __init__(self):
        self.table_model_map = self._generate_table_model_map()
        self.table_field_obj_map = self._generate_table_field_obj_map()

    @staticmethod
    def _generate_table_model_map():
        models_list = apps.get_models()
        table_model_map = {}

        for item in models_list:
            table_model_map[item._meta.db_table] = item

        return table_model_map

    def _generate_table_field_obj_map(self):
        table_field_obj_map = {}
        for table, model_class in self.table_model_map.items():
            table_field_obj_map[table] = {}

            fields_list = model_class._meta.get_fields()
            for field_obj in fields_list:
                if (field_obj.is_relation or field_obj.unique or field_obj.db_index or
                        type(field_obj) == models.BooleanField or type(field_obj) == models.NullBooleanField):
                    continue
                if hasattr(field_obj, 'db_column'):
                    field_name = field_obj.db_column if field_obj.db_column else field_obj.name

                table_field_obj_map[table][field_name] = field_obj

        return table_field_obj_map

    def is_valid_index(self, table, field):
        return True if self.table_field_obj_map[table].get(field) else False
