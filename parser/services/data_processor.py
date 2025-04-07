from typing import List, Dict
from django.http import QueryDict
from .api_service import ApiService
from .parsers import ParserInterface
import re

class DataProcessor:
    def __init__(self, api_service: ApiService, onu_data_parser: ParserInterface,
                 onu_stats_parser: ParserInterface):
        self.api_service = api_service
        self.onu_data_parser = onu_data_parser
        self.onu_stats_parser = onu_stats_parser

    def process(self, request: QueryDict) -> Dict:
        sort_field = request.get('sort_field', 'interface')
        sort_direction = request.get('sort_direction', 'asc')
        filters = request.get('filters', '[]')
        page = int(request.get('page', 1))
        per_page = int(request.get('per_page', 100))

        import json
        filters = json.loads(filters) if isinstance(filters, str) else filters

        # Получение данных
        onu_data_raw = self.api_service.get_onu_data()
        onu_stats_raw = self.api_service.get_onu_stats()

        # Парсинг
        onu_data = self.onu_data_parser.parse(onu_data_raw)
        onu_stats = self.onu_stats_parser.parse(onu_stats_raw)

        onu_data = [{**item, 'interface': item['interface'].lower()} for item in onu_data]
        onu_stats = [{**item, 'interface': item['interface'].lower()} for item in onu_stats]

        combined = []
        for data in onu_data:
            stat = next((s for s in onu_stats if s['interface'] == data['interface']), {})
            combined.append({**data, **stat})

        # Применение фильтров
        if filters:
            combined = self.apply_filters(combined, filters)

        # Сортировка
        combined = self.sort_data(combined, sort_field, sort_direction)

        # Пагинация
        total = len(combined)
        start = (page - 1) * per_page
        end = start + per_page
        data = combined[start:end]

        return {
            'data': data,
            'total': total,
            'page': page,
            'per_page': per_page,
            'last_page': (total + per_page - 1) // per_page
        }

    def apply_filters(self, data: List[Dict], filters: List[Dict]) -> List[Dict]:
        for filter in filters:
            field = filter.get('field')
            operator = filter.get('operator', '=')
            value = filter.get('value', '')
            if not field or value == '':
                continue

            data = [item for item in data if self.apply_filter(item, field, operator, value)]
        return data

    def apply_filter(self, item: Dict, field: str, operator: str, value: str) -> bool:
        if field not in item:
            return False

        item_value = item[field]
        is_numeric = field in ['temperature', 'voltage', 'bias', 'rx_power', 'tx_power']
        if is_numeric:
            try:
                item_value = float(item_value)
                value = float(value)
            except ValueError:
                return False

        if operator == '=':
            return item_value == value
        elif operator == '>':
            return item_value > value
        elif operator == '<':
            return item_value < value
        elif operator == '>=':
            return item_value >= value
        elif operator == '<=':
            return item_value <= value
        elif operator == 'contains':
            return value.lower() in str(item_value).lower()
        return True

    def sort_data(self, data: List[Dict], sort_field: str, sort_direction: str) -> List[Dict]:
        def sort_key(item):
            value = item.get(sort_field, '')
            if sort_field == 'interface':
                match = re.search(r'gpon0\/1:(\d+)', value)
                return int(match.group(1)) if match else 0
            if sort_field in ['temperature', 'voltage', 'bias', 'rx_power', 'tx_power']:
                try:
                    return float(value)
                except ValueError:
                    return 0
            return value

        reverse = sort_direction == 'desc'
        return sorted(data, key=sort_key, reverse=reverse)