from constants import *
import requests
import re


class GroupManager(object):
    def __init__(self):
        self._access_token = ACCESS_TOKEN

    def get_group_id(self, vk_url: str) -> int:
        group_id_match = re.search(r'vk.com/(?:club|)(\d+)', vk_url)

        if group_id_match:
            return int(group_id_match.group(1))

        group_name = vk_url.split('/')[-1]
        return self._fetch_group_id_by_name(group_name)

    def get_info_by_ids(self, group_ids: list[str]) -> list[dict]:
        """Максимальное число идентификаторов — 500."""
        api_url = 'https://api.vk.com/method/groups.getById'
        params = {
            'group_ids': ','.join(group_ids),
            'fields': 'members_count',
            'access_token': self._access_token,
            'v': '5.131'  # Версия API
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()

            if 'response' in data and data['response']:
                return data['response']
            else:
                print('Ошибка при получении ID сообщества:', data)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API ВКонтакте: {e}")
            return None

    def _fetch_group_id_by_name(self, group_name: str) -> int | None:
        api_url = 'https://api.vk.com/method/groups.getById'
        params = {
            'group_ids': group_name,
            'access_token': self._access_token,
            'v': '5.131'  # Версия API
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()

            if 'response' in data and data['response']:
                return data['response'][0]['id']
            else:
                print('Ошибка при получении ID сообщества:', data)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API ВКонтакте: {e}")
            return None

    def is_member(self, group_id: int, user_id: int) -> bool:
        api_url = 'https://api.vk.com/method/groups.isMember'
        params = {
            'group_id': group_id,
            'user_id': user_id,
            'access_token': self._access_token,
            'v': '5.131'
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'response' in data and 'member' in data['response']:
                return bool(data['response']['member'])
            else:
                print('Ошибка при проверке участия:', data)
                return False
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API ВКонтакте: {e}")
            return False