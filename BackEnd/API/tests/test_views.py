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

        # - PASSWORD
        # - - is in response
        self.assertTrue("password" in res.data)

        # - - is not stored in plain text
        self.assertNotEqual(res.data["password"], self.user_data["password"])

        # - URL
        # - - is sent response
        self.assertTrue("url" in res.data)

        # - - is not empty
        self.assertNotEqual(res.data["url"], "")

        # - USER ID
        # - - is sent back in response
        self.assertTrue("id" in res.data)

        # - - is not empty
        self.assertNotEqual(res.data["id"], "")

    def test_user_can_be_deleted_with_write_token(self):
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

        # - - is not empty
        # self.assertNotEqual(res.data["email"], "")

        # - BANK ID
        # - - is in response
        self.assertTrue("bank_id" in res.data)

        # - - is not empty
        self.assertNotEqual(res.data["bank_id"], "")

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

        # - PASSWORD
        # - - is in response
        self.assertTrue("password" in res.data[0].keys())

        # - - is not stored in plain text
        self.assertNotEqual(res.data[0]["password"], self.user_data["password"])

        # - URL
        # - - is sent response
        self.assertTrue("url" in res.data[0].keys())

        # - - is not empty
        self.assertNotEqual(res.data[0]["url"], "")

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
            "email": "test@gmail.com_MODIFIED"
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

    def test_mean_of_payment_unique_creation(self):
        """
        TWO MOP WITH THE SAME MOP IS IMPOSSIBLE
        """

        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Mean of payment creation
        mop_data = {
            "description": "mop_desc"
        }
        res = self.client.post(self.mop_url, mop_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_201_CREATED)

    def test_mean_of_payment_double_creation(self):
        """
        TWO MOP WITH THE SAME MOP IS IMPOSSIBLE
        """

        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Means of payment creations
        mop_data = {
            "description": "mop_desc"
        }
        res = self.client.post(self.mop_url, mop_data)

        res2 = self.client.post(self.mop_url, mop_data)

        # Status tests
        self.assertEqual(res.status_code, s.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, s.HTTP_400_BAD_REQUEST)

        # Because 2 mop can't have the same description (which is stends for signature of the mop)

    def test_payment_with_enough_money(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Bank id for the user
        bankID = tres.data["bank_id"]

        # Mean of payment creation
        mop_data = {
            "description": "mop_desc"
        }
        mopres = self.client.post(self.mop_url, mop_data)

        # Payment sending
        payment_data = {
            "money": "20",
            "mop_description": "mop_desc"
        }
        fullURL = self.bankaccount_url + "{}/".format(bankID)
        res = self.client.put(self.bankaccount_url + "{}/".format(bankID), payment_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_200_OK)

        # Body test

        # - BANK ID
        # - - is in response
        self.assertTrue("id" in res.data)

        # - - is correct
        self.assertEqual(res.data["id"], tres.data["bank_id"])

        # - MONEY LEFT
        # - - is in response
        self.assertTrue("id" in res.data)

        # - USER ID
        # - - is in response
        self.assertTrue("users_id" in res.data)

        # - - is correct
        self.assertEqual(res.data["users_id"], cres.data["id"])

    def test_payment_without_enough_money(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Bank id for the user
        bankID = tres.data["bank_id"]

        # Mean of payment creation
        mop_data = {
            "description": "mop_desc"
        }
        mopres = self.client.post(self.mop_url, mop_data)

        # Payment sending
        payment_data = {
            "money": "200",
            "mop_description": mop_data["description"]
        }
        fullURL = self.bankaccount_url + "{}/".format(bankID)
        res = self.client.put(self.bankaccount_url + "{}/".format(bankID), payment_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

        # Body test
        # - MONEY
        # - - is in response
        self.assertTrue("money" in res.data)

        # - - is correct
        self.assertEqual(str(res.data["money"][0]), "Not enough money")

    def test_payment_with_high_bill(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Bank id for the user
        bankID = tres.data["bank_id"]

        # Mean of payment creation
        mop_data = {
            "description": "mop_desc"
        }
        mopres = self.client.post(self.mop_url, mop_data)

        # Payment sending
        payment_data = {
            "money": "1200",
            "mop_description": mop_data["description"]
        }
        fullURL = self.bankaccount_url + "{}/".format(bankID)
        res = self.client.put(self.bankaccount_url + "{}/".format(bankID), payment_data)

        # Status test
        self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

        # Body test
        # - MONEY
        # - - is in response
        self.assertTrue("money" in res.data)

        # - - is correct
        self.assertEqual(str(res.data["money"][0]), "The bill is too high")

    def test_payment_with_bank_blocked(self):
        # User creation
        cres = self.client.post(self.user_url, self.user_data)

        # Token creation
        tres = self.client.post(self.token_url, self.user_data)

        # Token setting
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + tres.data["token"])

        # Bank id for the user
        bankID = tres.data["bank_id"]

        # Mean of payment creation
        mop_data = {
            "description": "mop_desc"
        }
        mopres = self.client.post(self.mop_url, mop_data)

        # Payment sending
        payment_data = {
            "money": "200",
            "mop_description": mop_data["description"]
        }
        fullURL = self.bankaccount_url + "{}/".format(bankID)

        for reiteration in [1,2,3,4]:
            res = self.client.put(self.bankaccount_url + "{}/".format(bankID), payment_data)

            # Status test
            self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

            # Body test
            # - MONEY
            # - - is in response
            self.assertTrue("money" in res.data)

            # - - is correct
            if reiteration < 3:
                self.assertEqual(str(res.data["money"][0]), "Not enough money")
            elif reiteration == 3:
                self.assertEqual(str(res.data["money"][0]), "Your bank account has been blocked")
            else:
                self.assertEqual(str(res.data["money"][0]), "Your bank account is blocked")




