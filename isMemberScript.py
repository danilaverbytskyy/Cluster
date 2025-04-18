from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserGroupService import UserGroupService
from database.UserService import UserService
from constants import DB_PASSWORD
import psycopg2

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

# Сбрасываем points для всех пользователей
cursor.execute("UPDATE users SET points = 0")
connection.commit()  # Фиксируем изменения

# Загружаем ID групп из файла
with open('GROUPS_Links.txt', 'r', encoding='utf-8') as f:
    groups_data = [group_manager.get_group_id(line.strip()) for line in f]

print(groups_data)

# Получаем всех пользователей из БД
cursor.execute("SELECT user_id, user_vk_id FROM users")
users = cursor.fetchall()  # Список кортежей (user_id, user_vk_id)

for group_id in groups_data:
    print(f"Проверяем группу: {group_id}")
    # Разбиваем пользователей на батчи по 500
    for i in range(0, len(users), 500):
        batch = users[i:i + 500]
        user_vk_ids = [user_vk_id for _, user_vk_id in batch]  # Извлекаем только VK ID
        # Получаем словарь: {user_vk_id: bool}
        membership_results = group_manager.is_members(group_id, user_vk_ids)

        # Обновляем points только для тех пользователей, которые состоят в группе
        for user_id, user_vk_id in batch:
            if membership_results.get(user_vk_id, False):
                cursor.execute(
                    "UPDATE users SET points = points + 1 WHERE user_id = %s",
                    (user_id,)
                )
    # Фиксируем изменения в БД
    connection.commit()

# Закрываем соединение
cursor.close()
connection.close()
