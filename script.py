from Models.User import User


vk_url = input("Введите ссылку на страницу ВКонтакте: \n")
user = User(vk_url)
friends = user.get_user_friends()
print(friends)
