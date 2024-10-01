from classes.User import User


vk_url = 'https://vk.com/glavnayytka'
print(vk_url)

user = User(vk_url)

friends = user.get_subscriptions()
print(friends)
