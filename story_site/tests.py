from django.test import TestCase
from populate_database import populate_countries

# Create your tests here.
class CreateTestDataBase(TestCase):
    def setUp(self):
        populate_countries()
    def test_nothing(self):
        self.assertEqual("a", "a")
