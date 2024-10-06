from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserService import UserService
from constants import DB_URL

group_service = GroupService(DB_URL, GroupManager())
group_service.add_groups([str(i) for i in range(500)])

user_service = UserService(DB_URL, UserManager())
user_service.add_users([str(i) for i in range(500)])
