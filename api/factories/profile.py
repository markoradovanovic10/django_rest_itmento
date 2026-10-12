import factory
from api.models import Profile
from api.factories import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
    user = factory.SubFactory(UserFactory)
    bio = factory.Faker('sentence')
    birth_date = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    location = factory.Faker('city')
    phone_number = factory.Faker('phone_number')
