from abc import ABC, abstractmethod
import re

class ParserInterface(ABC):
    @abstractmethod
    def parse(self, data: str) -> list:
        pass

class OnuDataParser(ParserInterface):
    def parse(self, data: str) -> list:
        lines = data.strip().split('\n')
        parsed = []
        current_record = ''
        data_started = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^GPON0\/1:\d+\s+', line):
                if current_record:
                    parsed.append(self.parse_record(current_record))
                current_record = line
                data_started = True
            elif data_started and 'OLT-Leninskoe-GPON#' in line:
                if current_record:
                    parsed.append(self.parse_record(current_record))
                break
            elif data_started:
                current_record += ' ' + line

        return parsed

    def parse_record(self, record: str) -> dict:
        columns = re.split(r'\s+', record.strip())
        if len(columns) < 7:
            return {}

        vendor_id = columns[1]
        if len(columns[1]) == 3 and re.match(r'^[A-Z]$', columns[2]):
            vendor_id += columns[2]
            columns.pop(2)

        sn = columns[3]
        if (len(columns) > 4 and columns[4] not in ['N/A', 'active', 'off-line', 'disabled']
            and ':' in columns[4]):
            sn += columns[4]
            columns.pop(4)

        active_time_index = next((i for i, col in enumerate(columns) if re.match(r'^\d{4}-\d{2}-\d{2}', col)), -1)

        return {
            'interface': columns[0],
            'vendor_id': vendor_id,
            'model_id': columns[2] if len(columns) > 2 else 'N/A',
            'sn': sn,
            'loid': columns[4] if len(columns) > 4 else 'N/A',
            'status': columns[5] if len(columns) > 5 else 'N/A',
            'config_status': columns[6] if len(columns) > 6 else 'N/A',
            'active_time': ' '.join(columns[active_time_index:]) if active_time_index != -1 else 'N/A',
        }

class OnuStatsParser(ParserInterface):
    def parse(self, data: str) -> list:
        lines = data.strip().split('\n')
        parsed = []
        current_record = ''
        data_started = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^gpon0\/1:\d+\s+', line):
                data_started = True

            if not data_started:
                continue

            if 'OLT-Leninskoe-GPON#' in line:
                if current_record and re.match(r'^gpon0\/1:\d+\s+', current_record):
                    parsed.append(self.parse_record(current_record))
                break

            if re.match(r'^gpon0\/1:\d+\s+', line):
                if current_record and re.match(r'^gpon0\/1:\d+\s+', current_record):
                    parsed.append(self.parse_record(current_record))
                current_record = line
            elif re.match(r'^gpon0\/', line):
                if current_record and re.match(r'^gpon0\/1:\d+\s+', current_record):
                    parsed.append(self.parse_record(current_record))
                current_record = line
            else:
                current_record += line

        if current_record and re.match(r'^gpon0\/1:\d+\s+', current_record) and current_record not in [r['interface'] for r in parsed]:
            parsed.append(self.parse_record(current_record))

        return [record for record in parsed if record]

    def parse_record(self, record: str) -> dict:
        fields = re.split(r'\s{2,}', record.strip())
        if len(fields) >= 6:
            return {
                'interface': fields[0],
                'temperature': fields[1],
                'voltage': fields[2],
                'bias': fields[3],
                'rx_power': fields[4],
                'tx_power': fields[5],
            }
        return {}