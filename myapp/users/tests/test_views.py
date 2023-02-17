
from django.test import TestCase, Client

# Create your tests here.


class TestRegularTests(TestCase):
    def test_index(self):
        client = Client()
        res = client.get(path='')
        self.assertEqual(res.status_code, 200)
