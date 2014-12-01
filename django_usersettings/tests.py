from django.test import TestCase
from django.contrib.auth import get_user_model

class DotNotationTestCase(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        UserModel.objects.create_user("jack")
        UserModel.objects.create_user("tom")    

    def test_get_unavailable_setting(self):
        UserModel = get_user_model()
        jack = UserModel.objects.get_by_natural_key('jack')
        with self.assertRaises(AttributeError):
            jack.settings.not_available

    def test_set_non_existant_setting(self):
        UserModel = get_user_model()
        jack = UserModel.objects.get_by_natural_key('jack')
        with self.assertRaises(AttributeError):
            jack.settings.non_existant
        jack.settings.non_existant = "something"
        self.assertEqual(jack.settings.non_existant, "something")

    def test_set_existing_setting(self):
        UserModel = get_user_model()
        jack = UserModel.objects.get_by_natural_key('jack')
        jack.settings.existing = "something"
        jack.settings.existing = "another thing"
        self.assertEqual(jack.settings.existing, "another thing")
        
