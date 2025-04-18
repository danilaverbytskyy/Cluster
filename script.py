from sqlite3 import Cursor
from xmlrpc.client import MAXINT
from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserGroupService import UserGroupService
from database.UserService import UserService
from constants import DB_URL
import sqlite3

USER_COUNT_LIMIT = 100000

user_manager = UserManager()
group_manager = GroupManager()
group_service = GroupService(DB_URL, GroupManager())
user_service = UserService(DB_URL, UserManager())
user_group_service = UserGroupService(DB_URL)

connect = sqlite3.connect('cluster.db')
cursor = connect.cursor()
cursor.execute("SELECT vk_id from users where id=(SELECT max(id) from users)")
result = cursor.fetchone()
last_user_id = result[0] if type(result) is tuple else 0

# all tables
# for j in range(last_user_id+1, MAXINT, 500):
#     # user_ids = [str(user_manager.get_id('https://vk.com/nagito_komaeda_my_beloved'))]
#     user_ids = [str(user_id) for user_id in range(j, j + 500)]
#     user_service.add_users([user_id for user_id in user_ids])
#     for user_id in user_ids:
#         subscriptions = user_manager.get_subscriptions(user_id)
#         if subscriptions is None:
#             continue
#         group_ids = subscriptions['groups']['items']
#         user_group_pairs = [(int(user_id), int(group_id)) for group_id in group_ids]
#         if user_group_pairs is None or len(user_group_pairs) == 0:
#             continue
#
#         # user_service.add_users([str(user_id)])
#         group_service.add_groups([str(elem) for elem in group_ids[0:500]])
#         user_group_service.add_user_groups(user_group_pairs)
#
#         last_user_id += 1
#         if last_user_id >= USER_COUNT_LIMIT:
#             break
#     if last_user_id >= USER_COUNT_LIMIT:
#         break

# only users
for j in range(last_user_id+1, USER_COUNT_LIMIT+1, 500):
    user_ids = [str(user_id) for user_id in range(j, j + 500)]
    user_service.add_users([user_id for user_id in user_ids])
