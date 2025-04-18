from database.DatabaseManager import DatabaseManager


class UserGroupService(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_user_groups(self, user_group_pairs: list[tuple[int, int]]) -> None:
        """
        Добавляет связи пользователь-группа в таблицу user_groups.
        Предотвращает дублирование записей.
        """
        try:
            insert_query = """
            INSERT INTO user_groups (user_id, group_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, group_id) DO NOTHING;
            """

            self.cursor.executemany(insert_query, user_group_pairs)
            self.connection.commit()
            print(f"✅ Добавлено {len(user_group_pairs)} связей пользователь-группа.")

        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при добавлении связей пользователь-группа: {e}")
