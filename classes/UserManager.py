from constants import *
import requests
import re


class UserManager(object):
    def __init__(self):
        self._access_token = ACCESS_TOKEN

    def get_id(self, vk_url: str) -> int:
        user_id = re.search(r'vk.com/(?:id|)(\d+)', vk_url)
        if user_id:
            user_id = user_id.group(1)
            return user_id
        else:
            # Если это не ID, возможно, это пользователь по имени
            username = vk_url.split('/')[-1]
            user_id = username

            # Запрос к API ВКонтакте для получения ID пользователя по имени
            api_url = 'https://api.vk.com/method/users.get'
            params = {
                'user_ids': username,
                'access_token': self._access_token,
                'v': '5.131'  # Версия API
            }

            response = requests.get(api_url, params=params)
            data = response.json()

            if 'response' in data:
                return data['response'][0]['id']
            else:
                print('Ошибка при получении ID пользователя:', data)
                return None

    def get_info(self, user_ids: list[str]) -> list[dict]:
        api_url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': ','.join(user_ids),
            'fields': 'sex,bdate,city,country,home_town,has_photo,photo_max_orig,online,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,occupation,nickname,relation,relatives,personal,connections,exports,activities,interests,music,movies,tv,books,games,about,quotes,timezone,career,military',
            'access_token': self._access_token,
            'v': '5.131',
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            return data['response']
        else:
            print('Ошибка при получении данных:', data)

    def get_friends(self, vk_url: str) -> dict:
        """Возвращает словарь с ключами count->int items->list"""
        user_id = self.get_id(vk_url)

        if user_id is None:
            return

        api_url = 'https://api.vk.com/method/friends.get'
        params = {
            'user_id': user_id,
            'access_token': self._access_token,
            'v': '5.131'
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            friends = data['response']
            return friends
        else:
            print('Ошибка при получении данных:', data)

    def get_subscriptions(self, vk_url: str):
        user_id = self.get_id(vk_url)

        if user_id is None:
            return

        api_url = 'https://api.vk.com/method/users.getSubscriptions'
        params = {
            'user_id': user_id,
            'access_token': self._access_token,
            'v': '5.131'
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            subscriptions = data['response']  # Получаем список идентификаторов подписок
            return subscriptions
        else:
            print('Ошибка при получении данных:', data)

    def is_closed(self, user_id: int):
        info = self.get_info([str(user_id)])
        return info[0]['is_closed']

    def is_private(self, user_id: int):
        info = self.get_info([str(user_id)])
        return 'is_private' in info[0].keys()
