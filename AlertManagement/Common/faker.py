from Registrations.methods import random_string
from Registrations.models import User
from django_faker import Faker

__author__ = 'Hp'

# this Populator is only a function thats return a django_faker.populator.Populator instance
# correctly initialized with a faker.generator.Generator instance, configured as above

populator = Faker.getPopulator()

populator.addEntity(User, 1, {
    'first_name': 'Osman',
    'last_name': 'Jamil',
    'email': 'osman@gmail.com',
    'moderator': 'weather',
    'password': 'abc123',
    'city': 'Lahore',
    'profile_img_path': '/static/img/default_profile_image.jpg',
    'bearer_token': random_string(32)
})

# populator.execute()

populator.addEntity(User, 1, {
    'first_name': 'Waqas',
    'last_name': 'Ismail',
    'email': 'waqas@gmail.com',
    'moderator': 'terrorism',
    'password': 'abc123',
    'city': 'Lahore',
    'profile_img_path': '/static/img/default_profile_image.jpg',
    'bearer_token': random_string(32)
})

# populator.execute()

populator.addEntity(User, 1, {
    'first_name': 'Javeria',
    'last_name': 'Janim',
    'email': 'javeria@gmail.com',
    'moderator': '',
    'password': 'abc123',
    'city': 'Lahore',
    'profile_img_path': '/static/img/default_profile_image.jpg',
    'bearer_token': random_string(32)
})

# populator.execute()

populator.addEntity(User, 1, {
    'first_name': 'Awais',
    'last_name': 'Jamil',
    'email': 'awais@gmail.com',
    'moderator': 'public',
    'city': 'Lahore',
    'password': 'abc123',
    'profile_img_path': '/static/img/default_profile_image.jpg',
    'bearer_token': random_string(32)
})

# populator.execute()

populator.addEntity(User, 1, {
    'first_name': 'Internet',
    'last_name': '',
    'email': 'internet@user.com',
    'moderator': 'internet',
    'password': 'hello123',
    'profile_img_path': '/static/img/internet.png',
    'city': '',
    'bearer_token': random_string(32)
})

# populator.execute()
