import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from models import UserSetting

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


class RestAPITestCase(TestCase):
    API_BASE = "/api/v1/settings/"
    def setUp(self):
        UserModel = get_user_model()
        jack = UserModel.objects.create_user("jack")
        jack.is_staff = True
        jack.save()

        jack.settings.aaa = True
        temp = UserSetting.objects.get(
            user = jack,
            field_name = "aaa")
        temp.label = "label for aaa"
        temp.field_type = UserSetting.TYPE_BOOL
        temp.save()

        jack.settings.bbb = "something"
        temp = UserSetting.objects.get(
            user = jack,
            field_name = "bbb")
        temp.label = "label for bbb"
        temp.field_type = UserSetting.TYPE_STRING
        temp.save()

        self.jack_pk = jack.pk
        self.current_jack_dict = {
            "aaa": {
                "label": "label for aaa",
                "type": "bool",
                "value": "True",
            },
            "bbb": {
                "label": "label for bbb",
                "type": "string",
                "value": "something",
            },
            "resource_uri": "/api/v1/settings/1/",
        }

        tom = UserModel.objects.create_user("tom")
        tom.is_staff = False
        tom.save()
        tom.settings.aaa = False
        tom.settings.bbb = "something"
        self.tom_pk = tom.pk

        jerry = UserModel.objects.create_user("jerry")
        jerry.is_staff = False
        jerry.save()
        jerry.settings.aaa = False
        jerry.settings.bbb = "another thing"
        self.jerry_pk = jerry.pk

        self.client = Client()
        
    def test_api_get_object(self):
        client = Client()
        response = client.get(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        self.assertJSONEqual(
            response.content,
            json.dumps(self.current_jack_dict),
        )

    def test_api_put_update(self):
        client = Client()
        response = client.put(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
            data = json.dumps({
                "aaa": {
                    "value": "False",
                    "label": "new label",
                    "type": "bool",
                    }}),
        )
        self.current_jack_dict['aaa']['value'] = 'False'
        self.current_jack_dict['aaa']['label'] = 'new label'
        response = client.get(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        self.assertJSONEqual(
            response.content,
            json.dumps(self.current_jack_dict),
        )
                             
    def test_api_put_insert(self):
        client = Client()
        response = client.put(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
            data = json.dumps({
                "ccc": {
                    "value": "25",
                    "label": "new setting",
                    "type": "number",
                    }}),
        )
        self.current_jack_dict['ccc'] = {
            'value': '25',
            'label': 'new setting',
            'type': 'number'}
        response = client.get(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        self.assertJSONEqual(
            response.content,
            json.dumps(self.current_jack_dict),
        )

    def test_api_patch_update(self):
        client = Client()
        response = client.patch(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
            data = json.dumps({
                "aaa": {
                    "value": "False",
                    "label": "new label",
                    "type": "bool",
                    }}),
        )
        self.current_jack_dict['aaa']['value'] = 'False'
        self.current_jack_dict['aaa']['label'] = 'new label'
        response = client.get(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        self.assertJSONEqual(
            response.content,
            json.dumps(self.current_jack_dict),
        )
                             
    def test_api_patch_delete(self):
        client = Client()
        response = client.patch(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
            data = json.dumps({
                "aaa": {
                    "value": None,
                    "label": "new label",
                    "type": "bool",
                    }}),
        )
        self.current_jack_dict.pop('aaa')
        response = client.get(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        self.assertJSONEqual(
            response.content,
            json.dumps(self.current_jack_dict),
        )
                             
    def test_api_delete(self):
        client = Client()
        response = client.delete(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        response = client.get(
            "%s%s/" % (RestAPITestCase.API_BASE, self.jack_pk),
            content_type='application/json',
        )
        self.current_jack_dict.pop('aaa')
        self.current_jack_dict.pop('bbb')
        self.assertJSONEqual(
            response.content,
            json.dumps(self.current_jack_dict),
        )

