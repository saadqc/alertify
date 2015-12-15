from Registrations.models import User
from django_faker import Faker

__author__ = 'Hp'

# this Populator is only a function thats return a django_faker.populator.Populator instance
# correctly initialized with a faker.generator.Generator instance, configured as above
populator = Faker.getPopulator()


populator.addEntity(User, 10000, {
    'password': 'abc123',
    'profile_img_path': '/static/img/default_profile_image.jpg'
})

# insertedPks = populator.execute()
