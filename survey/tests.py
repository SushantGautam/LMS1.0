import unittest
from django.urls import reverse
from django.test import Client
from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_categoryinfo(**kwargs):
    defaults = {}
    defaults["Category_Name"] = "Category_Name"
    defaults.update(**kwargs)
    return CategoryInfo.objects.create(**defaults)


def create_surveyinfo(**kwargs):
    defaults = {}
    defaults["Survey_Title"] = "Survey_Title"
    defaults["Survey_Cover"] = "Survey_Cover"
    defaults["Use_Flag"] = "Use_Flag"
    defaults.update(**kwargs)
    return SurveyInfo.objects.create(**defaults)


def create_questioninfo(**kwargs):
    defaults = {}
    defaults["Question_Name"] = "Question_Name"
    defaults.update(**kwargs)
    return QuestionInfo.objects.create(**defaults)


def create_optioninfo(**kwargs):
    defaults = {}
    defaults["Option_Name"] = "Option_Name"
    defaults.update(**kwargs)
    return OptionInfo.objects.create(**defaults)


class CategoryInfoViewTest(unittest.TestCase):
    '''
    Tests for CategoryInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_categoryinfo(self):
        url = reverse('categoryinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_categoryinfo(self):
        url = reverse('categoryinfo_create')
        data = {
            "Category_Name": "Category_Name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_categoryinfo(self):
        categoryinfo = create_categoryinfo()
        url = reverse('categoryinfo_detail', args=[categoryinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_categoryinfo(self):
        categoryinfo = create_categoryinfo()
        data = {
            "Category_Name": "Category_Name",
        }
        url = reverse('categoryinfo_update', args=[categoryinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class SurveyInfoViewTest(unittest.TestCase):
    '''
    Tests for SurveyInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_surveyinfo(self):
        url = reverse('surveyinfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_surveyinfo(self):
        url = reverse('surveyinfo_create')
        data = {
            "Survey_Title": "Survey_Title",
            "Survey_Cover": "Survey_Cover",
            "Use_Flag": "Use_Flag",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_surveyinfo(self):
        surveyinfo = create_surveyinfo()
        url = reverse('surveyinfo_detail', args=[surveyinfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_surveyinfo(self):
        surveyinfo = create_surveyinfo()
        data = {
            "Survey_Title": "Survey_Title",
            "Survey_Cover": "Survey_Cover",
            "Use_Flag": "Use_Flag",
        }
        url = reverse('surveyinfo_update', args=[surveyinfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QuestionInfoViewTest(unittest.TestCase):
    '''
    Tests for QuestionInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_questioninfo(self):
        url = reverse('questioninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_questioninfo(self):
        url = reverse('questioninfo_create')
        data = {
            "Question_Name": "Question_Name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_questioninfo(self):
        questioninfo = create_questioninfo()
        url = reverse('questioninfo_detail', args=[questioninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_questioninfo(self):
        questioninfo = create_questioninfo()
        data = {
            "Question_Name": "Question_Name",
        }
        url = reverse('questioninfo_update', args=[questioninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class OptionInfoViewTest(unittest.TestCase):
    '''
    Tests for OptionInfo
    '''
    def setUp(self):
        self.client = Client()

    def test_list_optioninfo(self):
        url = reverse('optioninfo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_optioninfo(self):
        url = reverse('optioninfo_create')
        data = {
            "Option_Name": "Option_Name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_optioninfo(self):
        optioninfo = create_optioninfo()
        url = reverse('optioninfo_detail', args=[optioninfo.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_optioninfo(self):
        optioninfo = create_optioninfo()
        data = {
            "Option_Name": "Option_Name",
        }
        url = reverse('optioninfo_update', args=[optioninfo.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)



