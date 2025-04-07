import requests
from requests.exceptions import RequestException
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ApiService:
    def __init__(self):
        self.base_url = 'https://exsrv.asarta.ru/api/test-task/'
        self.headers = {
            'Authorization': 'Bearer 213b7sHEbEqNqmbLbmRcaQ27HMsrzmMcQqT5THqU5cMLv0B',
            'Accept': 'text/plain',
        }

    def get_onu_data(self) -> str:
        try:
            response = requests.get(f'{self.base_url}get_onu_data.php', headers=self.headers, verify=False)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            raise Exception(f'Ошибка при получении ONU Data: {str(e)}')

    def get_onu_stats(self) -> str:
        try:
            response = requests.get(f'{self.base_url}get_onu_stats.php', headers=self.headers, verify=False)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            raise Exception(f'Ошибка при получении ONU Stats: {str(e)}')