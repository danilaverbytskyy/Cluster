from classes.User import User


vk_url = 'https://vk.com/molotovdanila'
print(vk_url)
user = User(vk_url)
friends = user.get_info()
print(friends)
