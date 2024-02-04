import factory
from faker import Faker
from src.models.item import Item
fake = Faker()


class ItemFactory(factory.Factory):
    """Create fake Account"""
    class Meta:
        """Persistent class for factory"""
        model = Item

    name = factory.Faker("name")
    description = fake.paragraph(nb_sentences=5)
    brand = factory.Faker('name')
