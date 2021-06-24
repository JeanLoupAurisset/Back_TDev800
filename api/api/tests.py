from django.test import TestCase
from myapp.models import album

class AnimalTestCase(TestCase):
    """
    class album(models.Model):
        id_album = models.IntegerField(primary_key=True)
        nom = models.CharField(max_length=50)
    """
    def setUp(self):
        album.objects.create(nom="lion")
        album.objects.create(nom="cat")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = album.objects.get(nom="lion")
        cat = album.objects.get(nom="cat")
        self.assertEqual(lion.get_album(), 'lion')
        self.assertEqual(cat.get_album(), 'cat')