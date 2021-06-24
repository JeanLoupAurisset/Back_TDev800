from rest_framework.test import APITestCase, APIClient
#from django.urls import reverse
from ..urls import router
from ..views import *
from rest_framework import reverse

class TestSetUp(APITestCase):
    """
    Notice that setUp and tearDown are called before each tests
    """
    def setUp(self):
        self.user_url = "/user/"
        self.bankaccount_url = "/bank_account/"
        self.token_url = "/api-token-auth/"
        self.user_logout_url = "/user/logout/"
        self.mop_url = "/mop/"

        self.user_data ={
            "username":"userTest",
            "email":"test@gmail.com",
            "password":"password"
        }

        return super().setUp()




    def tearDown(self):
        return super().tearDown()
