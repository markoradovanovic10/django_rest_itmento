from django.core.management.base import BaseCommand
from ...models import Item
from ...factories.item import ItemFactory
from ...factories.user import UserFactory
from ...factories.profile import ProfileFactory

class Command(BaseCommand):

    help = 'Test the ItemFactory'

    def handle(self, *args, **options):
        ItemFactory.create_batch(5)
        UserFactory.create_batch(2)

        ProfileFactory.create_batch(2)


        self.stdout.write('Testing ItemFactory...')