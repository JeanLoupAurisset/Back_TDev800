from .test_setup import TestSetUp
from rest_framework import status as s

"""
#DEBUGGER
import pdb
pdb.set_trace()

#Print response status code
res.status_code

#Print response data
res.data 

#Access to a specific info from response body
res.data['info']
"""


class TestViews(TestSetUp):

    def test_user_cannot_be_created_without_data(self):
        # User creation
        res = self.client.post(self.user_url)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

    def test_user_can_be_created_with_correct_data(self):
        # User creation
        res = self.client.post(self.user_url, self.user_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_201_CREATED)

        # Body test

        # - USERNAME
        # - - is in response
        self.assertTrue("username" in res.data)

        # - - is correct
        self.assertEqual(res.data["username"], self.user_data["username"])

        # - USER ID
        # - - is sent back in response
        self.assertTrue("id" in res.data)

        # - - is not empty
        self.assertNotEqual(res.data["id"], "")

    def test_user_can_be_deleted_with_right_token(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Delete user
        res = self.client.delete(self.user_url + "{}/".format(cres.data["id"]))

        # Status code
        self.assertEqual(res.status_code, s.HTTP_204_NO_CONTENT)

    def test_user_cant_be_deleted_with_incorrect_token(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "")

        # Delete user
        res = self.client.delete(self.user_url + "{}/".format(cres.data["id"]))

        # Status code
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_user_token_can_be_obtained(self):
        # User creation
        self.client.post(self.user_url, self.user_data)

        # Token creation
        res = self.client.post(self.token_url, self.user_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_200_OK)

        # Body test

        # - TOKEN
        # - - is in response
        self.assertTrue("token" in res.data)

        # - - is not empty
        self.assertNotEqual(res.data["token"], "")

        # - USER ID
        # - - is in response
        self.assertTrue("user_id" in res.data)

        # - - is not empty
        self.assertNotEqual(res.data["user_id"], "")

        # - EMAIL
        # - - is in response
        self.assertTrue("email" in res.data)

    def test_user_token_not_set_without_user_data(self):
        # Token creation
        res = self.client.post(self.token_url)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

    def test_get_all_users_infos_right_credentials(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # User info getter
        res = self.client.get(self.user_url)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_200_OK)

        # Body test
        # - USERNAME
        # - - is in response
        self.assertTrue("username" in res.data[0].keys())

        # - - is correct
        self.assertEqual(res.data[0]["username"], self.user_data["username"])

        # - USER ID
        # - - is sent back in response
        self.assertTrue("id" in res.data[0].keys())

        # - - is not empty
        self.assertNotEqual(res.data[0]["id"], "")

    def test_get_all_users_infos_incorrect_credentials(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "")

        # User info getter
        res = self.client.get(self.user_url)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_user_logout_destroy_token_with_right_credentials(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Destroy token
        res = self.client.get(self.user_logout_url)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_200_OK)

    def test_user_logout_destroy_token_with_incorrect_credentials(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "")

        # Destroy token
        res = self.client.get(self.user_logout_url)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_user_modify_informations_with_right_credentials(self):
        mod_data = {
            "username": "userTest_MODIFIED",
        }

        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # User modification
        res = self.client.put(self.user_url + "{}/".format(cres.data["id"]), mod_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_200_OK)

    def test_user_modify_informations_with_incorrect_credentials(self):
        mod_data = {
            "first_name": "test",
            "username": "userTest_MODIFIED",
            "email": "test@gmail.com_MODIFIED"
        }

        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "")

        # User modification
        res = self.client.put(self.user_url + "{}/".format(cres.data["id"]), mod_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_user_can_modify_his_password(self):
        None
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Modify password
        mod_passsord = {
            "old_password": "password",
            "new_password": "password_MODIFIED"
        }
        res = self.client.post(self.user_url + "{}/set_password/".format(cres.data["id"]), mod_passsord)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_200_OK)

        # Body test
        self.assertEqual(res.data["status"], "password set")

    def test_user_cant_modify_someone_else_password(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "hgtc6uv6byacv43vinoa0nuiaybi5vatc1")

        # Modify password
        mod_passsord = {
            "old_password": "password",
            "new_password": "password_MODIFIED"
        }
        res = self.client.post(self.user_url + "{}/set_password/".format(cres.data["id"]), mod_passsord)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)