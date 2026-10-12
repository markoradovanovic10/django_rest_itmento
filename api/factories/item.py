import factory
from ..models import Item

class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
