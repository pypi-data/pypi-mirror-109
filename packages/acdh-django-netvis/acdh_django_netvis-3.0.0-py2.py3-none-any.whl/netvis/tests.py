from django.test import TestCase


class ExampleTestCase(TestCase):

    def setUp(self):
        # Test definitions as before.
        pass

    def test_001_smoke(self):
        smoke = 'hot'
        self.assertEqual(smoke, 'hot')
