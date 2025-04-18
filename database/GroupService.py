from database.DatabaseManager import DatabaseManager
from classes.GroupManager import GroupManager

class GroupService(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.group_manager = GroupManager()

    def add_groups(self, group_ids: list[str]) -> None:
        """
        Принимает список строковых id групп.
        Получает информацию о группах через GroupManager.get_info_by_ids
        и добавляет их в БД. Если группа уже существует, дублирование не происходит.
        """
        try:
            groups_info = self.group_manager.get_info_by_ids(group_ids)
            if not groups_info:
                print("❌ Не удалось получить информацию о группах.")
                return

            insert_query = """
            INSERT INTO groups (group_vk_id, name, members_count, is_closed)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (group_vk_id) DO NOTHING;
            """

            for group in groups_info:
                group_vk_id = group.get("id")
                name = group.get("name")
                members_count = group.get("members_count", 0)
                is_closed = bool(group.get("is_closed", False))  # Преобразование в bool

                self.cursor.execute(insert_query, (group_vk_id, name, members_count, is_closed))

            self.connection.commit()
            print("✅ Группы успешно добавлены в базу данных.")

        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при добавлении групп: {e}")
