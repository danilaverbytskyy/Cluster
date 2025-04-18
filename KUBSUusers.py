from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserGroupService import UserGroupService
from database.UserService import UserService
from constants import DB_URL, DB_PASSWORD
import psycopg2

db_url = DB_URL

# Инициализация менеджеров и сервисов
user_manager = UserManager()
group_manager = GroupManager()
group_service = GroupService()
user_service = UserService(user_manager)
user_group_service = UserGroupService()

# Подключение к базе данных через psycopg2
connection = psycopg2.connect(
    dbname="cluster",
    user="postgres",
    password=DB_PASSWORD,
    host="localhost",
    port="5432"
)
cursor = connection.cursor()


def store_kubsu_users():
    kubsu_students_ids = group_manager.get_members(137765556)
    for p in range(0, len(kubsu_students_ids), 500):
        user_service.add_users([str(i) for i in kubsu_students_ids[p:p + 500]])

# store_kubsu_users()

cursor.execute("SELECT user_vk_id FROM users WHERE user_id>=(SELECT max(user_id) from user_groups)")
kubsu_vk_ids = [str(i[0]) for i in cursor.fetchall()]

for vk_id in kubsu_vk_ids:
    subscriptions = user_manager.get_subscriptions(vk_id)
    if not subscriptions:
        continue

    group_vk_ids = subscriptions['groups']['items']

    # Получаем user_id
    cursor.execute("SELECT user_id FROM users WHERE user_vk_id = %s", (vk_id,))
    user_result = cursor.fetchone()
    if not user_result:
        continue
    user_id = user_result[0]

    # Добавляем группы пачками по 500
    for i in range(0, len(group_vk_ids), 500):
        group_service.add_groups([str(elem) for elem in group_vk_ids[i:i + 500]])

    # Оптимизированный запрос - получаем group_id одним запросом
    cursor.execute(
        "SELECT group_id FROM groups WHERE group_vk_id IN %s",
        (tuple(group_vk_ids),)
    )
    group_ids = [row[0] for row in cursor.fetchall()]

    # Добавляем связи пользователей и групп
    user_group_pairs = [(user_id, group_id) for group_id in group_ids]

    if user_group_pairs:  # Проверяем, есть ли данные для вставки
        for i in range(0, len(user_group_pairs), 500):
            user_group_service.add_user_groups(user_group_pairs[i:i + 500])
