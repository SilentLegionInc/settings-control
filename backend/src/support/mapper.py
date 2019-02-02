from dateutil import parser


class Mapper:
    @staticmethod
    def map_get_monitoring_data_request(body):
        # TODO validate body
        return {
            'field_name': body['field_name'],
            'filter_params': {
                'start_time': parser.parse(body['start_time']) if body.get('start_time') else None,
                'end_time': parser.parse(body['end_time']) if body.get('end_time') else None
            },
            'additional_params': {
                'limit': body.get('limit'),
                'offset': body.get('offset')
            }
        }

    @staticmethod
    def map_get_monitoring_data_response(body):
        return {
            'result': list(map(lambda elem: {
                'value': elem['value'],
                'time': elem['time'].isoformat(),
                'latitude': elem['latitude'],
                'longitude': elem['longitude']
            }, body['result'])),
            'count': body['count'],
            'minimum': body['minimum'],
            'average': body['average'],
            'maximum': body['maximum']
        }

    @staticmethod
    def map_get_monitoring_logs_request(body):
        # TODO validate body
        return {
            'filter_params': {
                'start_time': parser.parse(body['start_time']) if body.get('start_time') else None,
                'end_time': parser.parse(body['end_time']) if body.get('end_time') else None,
                'type': body.get('type'),
            },
            'sort_params': {
                'type': body.get('sort_by_type'),
                'time': body.get('sort_by_time')
            },
            'additional_params': {
                'limit': body.get('limit'),
                'offset': body.get('offset')
            }
        }

    @staticmethod
    def map_get_monitoring_logs_response(body):
        return {
            'result': list(map(lambda elem: {
                'message': elem['message'],
                'time': elem['time'].isoformat(),
                'title': elem['title'],
                'type': elem['type']
            }, body['result'])),
            'count': body['count']
        }
