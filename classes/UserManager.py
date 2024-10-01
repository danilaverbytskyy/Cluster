from constants import *
import requests
import re


class UserManager:
    def __init__(self):
        self._access_token = ACCESS_TOKEN

    def get_id(self, vk_url) -> int:
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

    def get_info_one(self, vk_url: str):
        # Извлекаем ID пользователя из ссылки
        user_id = self.get_id(vk_url)

        # Запрос к API ВКонтакте
        api_url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': user_id,
            'access_token': self._access_token,
            'v': '5.131'
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            return data['response']
        else:
            print('Ошибка при получении данных:', data)

    def get_info_many(self, user_ids: list[str]):
        api_url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': ','.join(user_ids),
            'access_token': self._access_token,
            'v': '5.131'
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            return data['response']
        else:
            print('Ошибка при получении данных:', data)

    def get_friends(self, vk_url: str):
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
