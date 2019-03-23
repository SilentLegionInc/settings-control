from dateutil import parser


class Mapper:
    @staticmethod
    def map_get_monitoring_data_structure_response(body):
        return list(map(lambda elem: {
                'system_name': elem['system_name'],
                'name': elem['name'],
                'type': elem['type']
        }, body))

    @staticmethod
    def map_get_monitoring_databases_info_response(body):
        result = {}
        for key, value in body.items():
            result[key] = value
        return result

    @staticmethod
    def map_monitoring_chart_data_result(result):
        return list(map(lambda elem: {
            'id': elem['id'],
            'value': elem['value'],
            'time': elem['time'].isoformat(),
            'latitude': elem['latitude'],
            'longitude': elem['longitude']
        }, result))

    @staticmethod
    def map_get_monitoring_init_chart_data_response(body):
        return {
            'result': Mapper().map_monitoring_chart_data_result(body['result']),
            'min_time': body['min_time'].isoformat(),
            'max_time': body['max_time'].isoformat(),
            'interval_start_time': body['interval_start_time'].isoformat(),
            'interval_end_time': body['interval_end_time'].isoformat(),
            'minimum': body['minimum'],
            'average': body['average'],
            'maximum': body['maximum']
        }

    @staticmethod
    def map_get_monitoring_filter_chart_data_request(body):
        return {
            'min_time': parser.parse(body['min_time']),
            'max_time': parser.parse(body['max_time']),
            'interval_size': body['interval_size']
        }

    @staticmethod
    def map_get_monitoring_filter_chart_data_response(body):
        return {
            'result': Mapper().map_monitoring_chart_data_result(body['result']),
            'interval_start_time': body['interval_start_time'].isoformat(),
            'interval_end_time': body['interval_end_time'].isoformat(),
            'minimum': body['minimum'],
            'average': body['average'],
            'maximum': body['maximum']
        }

    @staticmethod
    def map_get_monitoring_page_chart_data_request(body):
        return {
            'interval_start_time': parser.parse(body['interval_start_time']),
            'interval_end_time': parser.parse(body['interval_end_time'])
        }

    @staticmethod
    def map_get_monitoring_page_chart_data_response(body):
        return {
            'interval_start_time': body['interval_start_time'],
            'interval_end_time': body['interval_end_time']
        }

    @staticmethod
    def map_get_monitoring_logs_request(body):
        def map_filter(obj):
            return {
                'start_time': parser.parse(obj['start_time']) if obj.get('start_time') else None,
                'end_time': parser.parse(obj['end_time']) if obj.get('end_time') else None,
                'type': obj.get('type')
            }

        def map_sort(obj):
            return_value = {}
            if obj.get('type'):
                return_value['type'] = 'ASC' if obj['type'] == 1 else 'DESC'
            if obj.get('time'):
                return_value['time'] = 'ASC' if obj['time'] == 1 else 'DESC'
            return return_value

        # TODO validate body
        return {
            'filter_params': map_filter(body.get('filter', {})),
            'sort_params': map_sort(body.get('sort', {})),
            'additional_params': {
                'limit': body.get('limit'),
                'offset': body.get('offset')
            }
        }

    @staticmethod
    def map_get_monitoring_logs_response(body):

        def map_result(result):
            return list(map(lambda elem: {
                'id': elem['id'],
                'message': elem['message'],
                'time': elem['time'].isoformat(),
                'title': elem['title'],
                'type': elem['type']
            }, result))

        return {
            'result': map_result(body['result']),
            'count': body['count']
        }

    @staticmethod
    def map_get_monitoring_table_data_request(robot_name, db_name, body):
        def map_filter(request_body, fields):
            body_filter = request_body.get('filter', {})
            filter_params_min = {
                'min__' + field_name: body_filter['min__' + field_name] for field_name in fields if body_filter.get('min__' + field_name)
            }
            filter_params_max = {
                'max__' + field_name: body_filter['max__' + field_name] for field_name in fields if body_filter.get('max__' + field_name)
            }
            filter_params = {
                'start_time': parser.parse(body_filter['start_time']) if body_filter.get('start_time') else None,
                'end_time': parser.parse(body_filter['end_time']) if body_filter.get('end_time') else None,
                'latitude': body_filter['latitude'] if body_filter.get('latitude') else None,
                'longitude': body_filter['longitude'] if body_filter.get('longitude') else None
            }
            filter_params.update(filter_params_min)
            filter_params.update(filter_params_max)

            return filter_params

        def map_sort(request_body, fields):
            body_sort = request_body.get('sort', {})
            sort_params = {
                field_name: ('ASC' if body_sort[field_name] == 1 else 'DESC') for field_name in fields if body_sort.get(field_name)
            }
            if body_sort.get('time'):
                sort_params['time'] = 'ASC' if body_sort['time'] == 1 else 'DESC'

            return sort_params

        from monitoring.monitoring_data_service import MonitoringDataService
        field_names = list(map(
                lambda elem: elem['system_name'],
                MonitoringDataService.get_data_structure(robot_name, db_name)
        ))

        # TODO validate body
        return {
            'filter_params': map_filter(body, field_names),
            'sort_params': map_sort(body, field_names),
            'additional_params': {
                'limit': body.get('limit'),
                'offset': body.get('offset'),
                'extended': body.get('extended')
            }
        }

    @staticmethod
    def map_get_monitoring_table_data_response(body, db_name):
        def map_result(result, structure):
            field_names = list(map(lambda struct_elem: struct_elem['system_name'], structure))
            return_value = []
            for elem in result:
                obj_to_add = {field_name: elem[field_name] for field_name in field_names}
                obj_to_add['time'] = elem['time'].isoformat()
                obj_to_add['latitude'] = elem['latitude']
                obj_to_add['longitude'] = elem['longitude']
                return_value.append(obj_to_add)
            return return_value

        def map_data_structure(structure):
            return list(map(lambda elem: {
                'system_name': elem['system_name'],
                'name': elem['name'],
                'type': elem['type']
            }, structure))

        return_val = {
            'result': map_result(body['result'], body['data_structure']),
            'count': body['count']
        }
        if body['extended']:
            return_val['data_structure'] = map_data_structure(body['data_structure'])

        return return_val

    @staticmethod
    def map_get_monitoring_maps_data_response(body):

        def map_points(points):
            result = []
            for elem in points:
                result_elem = {
                    'latitude': elem['latitude'],
                    'longitude': elem['longitude'],
                    'count': elem['count'],
                    'average': {}
                }
                for key, value in elem['average'].items():
                    result_elem['average'][key] = value
                result.append(result_elem)
            return result

        return {
            'points': map_points(body['points']),
            'center_latitude': body['center_latitude'],
            'center_longitude': body['center_longitude']
        }

    @staticmethod
    def map_get_numeric_fields_response(body):
        return list(
            map(lambda elem: {'name': elem['name'], 'system_name': elem['system_name']}, body)
        )
