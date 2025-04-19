from xmlrpc.client import MAXINT

from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserGroupService import UserGroupService
from database.UserService import UserService
from constants import DB_URL
import psycopg2

db_url = DB_URL

USER_COUNT_LIMIT = 10000

# Инициализация менеджеров и сервисов
user_manager = UserManager()
group_manager = GroupManager()
group_service = GroupService()
user_service = UserService(db_url)
user_group_service = UserGroupService()

# Подключение к базе данных через psycopg2
connection = psycopg2.connect(
    dbname="cluster",
    user="postgres",
    password="3dh1z6",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Получение последнего user_id
cursor.execute("SELECT vk_id FROM users WHERE id=(SELECT MAX(id) FROM users)")
result = cursor.fetchone()
last_user_id = result[0] if result else 0

#all tables
for j in range(last_user_id+1, MAXINT, 500):
    # user_ids = [str(user_manager.get_id('https://vk.com/nagito_komaeda_my_beloved'))]
    # user_service.add_users([user_id for user_id in user_ids])
    user_ids = [str(user_id) for user_id in range(j, j + 500)]
    for user_id in user_ids:
        subscriptions = user_manager.get_subscriptions(user_id)
        if subscriptions is None:
            continue
        group_ids = subscriptions['groups']['items']
        user_group_pairs = [(int(user_id), int(group_id)) for group_id in group_ids]
        if user_group_pairs is None or len(user_group_pairs) == 0:
            continue

        user_service.add_users([str(user_id)])
        for i in range(0, len(group_ids)+1, 500):
            group_service.add_groups([str(elem) for elem in group_ids[i:i+500]])
        user_group_service.add_user_groups(user_group_pairs)

    cursor.execute("SELECT vk_id FROM users WHERE id=(SELECT MAX(id) FROM users)")
    result = cursor.fetchone()
    last_user_id = result[0] if result else 0
    if last_user_id >= USER_COUNT_LIMIT:
        break

# Обработка только пользователей
# for j in range(last_user_id + 1, USER_COUNT_LIMIT + 1, 500):
#     user_ids = [str(user_id) for user_id in range(j, j + 500)]
#     user_service.add_users([user_id for user_id in user_ids])

# Закрытие соединения
cursor.close()
connection.close()
