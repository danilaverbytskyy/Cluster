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
                db_user = User(
                    vk_id=single_user_information['id'],
                    first_name=single_user_information['first_name'],
                    last_name=single_user_information['last_name'],
                    sex=single_user_information['sex'],
                    is_closed=single_user_information['is_closed'],
                    date_of_recording=datetime.now(),

                    # New attributes mapping
                    bdate=single_user_information.get('bdate'),
                    city=single_user_information.get('city', {}).get('title') if single_user_information.get(
                        'city') else None,
                    country=single_user_information.get('country', {}).get('title') if single_user_information.get(
                        'country') else None,
                    home_town=single_user_information.get('home_town'),
                    photo_max_orig=single_user_information.get('photo_max_orig'),
                    status=single_user_information.get('status'),
                    last_seen=datetime.fromtimestamp(
                        single_user_information['last_seen']['time']) if single_user_information.get(
                        'last_seen') else None,
                    followers_count=single_user_information.get('followers_count'),
                    occupation=single_user_information.get('occupation', {}).get('name') if single_user_information.get(
                        'occupation') else None,
                    relation=single_user_information.get('relation')
                )

                db_session.add(db_user)

            db_session.commit()
