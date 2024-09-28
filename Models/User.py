from constants import *
import requests
import re


class User:
    def __init__(self, vk_url: str):
        self.access_token = ACCESS_TOKEN
        self.id = self._get_id(vk_url)

    def _get_id(self, vk_url) -> int:
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
                'access_token': self.access_token,
                'v': '5.131'  # Версия API
            }

            response = requests.get(api_url, params=params)
            data = response.json()

            if 'response' in data:
                return data['response'][0]['id']
            else:
                print('Ошибка при получении ID пользователя:', data)
                return None

    def get_user_info(self):
        # Извлекаем ID пользователя из ссылки
        user_id = self.id

        # Запрос к API ВКонтакте
        api_url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': user_id,
            'access_token': self.access_token,
            'v': '5.131'
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            with open('data.txt', 'a') as file:
                file.write('\n' + str(data['response'][0]))
        else:
            print('Ошибка при получении данных:', data)

    def get_user_friends(self):
        user_id = self.id

        if user_id is None:
            return

        api_url = 'https://api.vk.com/method/friends.getLists'
        params = {
            'user_id': user_id,
            'access_token': self.access_token,
            'v': '5.131'
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'response' in data:
            friends = data['response']
            return friends
        else:
            print('Ошибка при получении данных:', data)
