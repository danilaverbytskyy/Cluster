from classes.GroupManager import GroupManager
from database.DatabaseManager import DatabaseManager
from models import Group


class GroupService(DatabaseManager):
    def __init__(self, db_url: str, group_manager: GroupManager):
        super().__init__(db_url)
        self.group_manager = group_manager

    def add_groups(self, group_ids: list[str]) -> None:
        with self.Session() as db_session:
            groups_info = self.group_manager.get_info_by_ids(group_ids)
            db_groups_info = [
                Group(
                    vk_id=single_group_information['id'],
                    name=single_group_information['name'],
                    members_count=single_group_information.get('members_count', 0),
                    is_closed=bool(single_group_information['is_closed'])
                ) for single_group_information in groups_info
            ]
            db_session.add_all(db_groups_info)
            db_session.commit()