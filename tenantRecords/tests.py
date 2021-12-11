from django.test import TestCase
import models

# Create your tests here.
class TestShopCase(TestCase):
    fixtures = ['test-data.json']

    def test_shopname(self):
        """test name is what you enter"""
        prim = models.Shop.objects.all()
        print prim
        self.assertEqual(prim[0].rent, prim[0].rent)