from database.DatabaseManager import DatabaseManager
from models import UserGroup


class UserGroupService(DatabaseManager):
    def __init__(self, db_url):
        super().__init__(db_url)

    def add_user_groups(self, user_group_pairs: list[tuple[int, int]]) -> None:
        with self.Session() as db_session:
            user_group_entries = [
                UserGroup(user_id=user_id, group_id=group_id)
                for user_id, group_id in user_group_pairs
            ]
            db_session.add_all(user_group_entries)
            db_session.commit()
