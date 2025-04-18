from datetime import datetime
from database.DatabaseManager import DatabaseManager
from classes.UserManager import UserManager


class UserService(DatabaseManager):
    def __init__(self, user_manager: UserManager):
        super().__init__()
        self.user_manager = user_manager

    def add_users(self, user_ids: list[str]) -> None:
        """
        Добавляет пользователей в базу данных.
        Если пользователь уже существует (по user_vk_id), он не дублируется.
        """
        try:
            users_info = self.user_manager.get_info(user_ids)
            if not users_info:
                print("❌ Не удалось получить данные пользователей.")
                return

            insert_query = """
            INSERT INTO users (
                user_vk_id, first_name, last_name, sex, is_closed, birth_date, 
                city, last_seen, followers_count, occupation, relation, date_of_recording, points
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0
            ) ON CONFLICT (user_vk_id) DO NOTHING;
            """

            for user_data in users_info:
                user_vk_id = user_data.get("id")
                first_name = user_data.get("first_name")
                last_name = user_data.get("last_name")
                sex = user_data.get("sex")
                is_closed = user_data.get("is_closed", False)
                birth_date = user_data.get("bdate")
                city = user_data.get("city", {}).get("title") if "city" in user_data else None
                last_seen = (
                    datetime.fromtimestamp(user_data["last_seen"]["time"]).date()
                    if "last_seen" in user_data else None
                )
                followers_count = user_data.get("followers_count", 0)
                occupation = user_data.get("occupation", {}).get("name") if "occupation" in user_data else None
                relation = user_data.get("relation")

                # Выполняем вставку в БД
                self.cursor.execute(insert_query, (
                    user_vk_id, first_name, last_name, sex, is_closed, birth_date,
                    city, last_seen, followers_count, occupation, relation
                ))

            self.connection.commit()
            print("✅ Пользователи успешно добавлены в базу данных.")

        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при добавлении пользователей: {e}")
