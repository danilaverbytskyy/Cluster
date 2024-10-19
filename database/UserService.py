from datetime import datetime
from database.DatabaseManager import DatabaseManager
from classes.UserManager import UserManager
from models import User


class UserService(DatabaseManager):
    def __init__(self, db_url: str, user_manager: UserManager):
        super().__init__(db_url)
        self.user_manager = user_manager

    def add_users(self, user_ids: list[str]) -> None:
        with self.Session() as db_session:
            users_info = self.user_manager.get_info(user_ids)
            for single_user_information in users_info:
                db_users_info = [
                    User(
                        vk_id=single_user_information['id'],
                        first_name=single_user_information['first_name'],
                        last_name=single_user_information['last_name'],
                        sex=single_user_information['sex'],
                        is_closed=single_user_information['is_closed'],
                        date_of_recording=datetime.now()
                    )
                ]
                db_session.add_all(db_users_info)
                db_session.commit()
