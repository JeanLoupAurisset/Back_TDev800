from .test_setup import TestSetUp
from rest_framework import status as s
from API.models import MeansOfPayment, User, BankAccount
from random import randint


class TestModel(TestSetUp):
    def test_user_creation(self):
        # User creation
        userID = randint(1, 10)
        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # Get user
        usr = User.objects.get(username="userTest")

        # ID
        # - is not null
        self.assertNotEqual(usr.id, "")

        # - is correct
        self.assertEqual(userID, usr.id)

        # EMAIL
        # - is correct
        self.assertEqual(usr.email, self.user_data["email"])

        # PASSWORD
        # - is not stored plain text
        self.assertNotEquals(usr.password, self.user_data["password"])

        # - is correct
        self.assertTrue(usr.check_password("password"))

    def test_user_modification(self):
        # User creation
        userID = randint(1, 10)
        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # Get user 1
        usr = User.objects.get(id=userID)

        # MODIFY
        # - Username
        usr.username = "userTest_MODIFIED"

        # - Email
        usr.email = "email_MODIFIED"

        # - Password
        usr.password = "password_MODIFIED"

        usr.save()

        # Get user 2
        usr2 = User.objects.get(id=userID)

        # Username test
        self.assertEqual(usr2.username, usr.username)

        # Password test
        self.assertEqual(usr2.password, usr.password)

        # Email test
        self.assertEqual(usr2.email, usr.email)

    def test_user_delete(self):
        # User creation
        userID = randint(1, 10)

        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # Get user
        usr = User.objects.get(id=userID)

        # Delete user
        usr.delete()

        # Get user list
        usrList = User.objects.all()

        # Delete test
        self.assertFalse("username" in usrList.values_list("username",flat=True))




    def test_means_of_payment_creation(self):

        # User creation
        userID = randint(1, 10)
        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # User getting
        usr = User.objects.get(id=userID)

        # Mop creation
        mopID = randint(1,10)
        mop_data = {
            "description": "mop_desc",
            "user_id": userID
        }
        MeansOfPayment.objects.create(id=mopID, description="desc", users_id=mop_data["user_id"])

        # Mop getting
        mop = MeansOfPayment.objects.get(id=mopID)

        # USER ID
        # - is correct
        self.assertEqual(mop.users_id,usr.id)

        # DESCRIPTION
        # - is correct
        self.assertEqual(mop.description, mop.description)

        # ID
        # - id correct
        self.assertEqual(mop.id, mopID)

    def test_bank_account_creation(self):
        # User creation
        userID = randint(1, 10)
        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # User getting
        usr = User.objects.get(id=userID)

        # Bank account creation
        baID = randint(1,10)
        BankAccount.objects.create(id = baID, users_id = userID)

        # Bank account getting
        ba = BankAccount.objects.get(id = baID)

        # USER IS
        # - is correct
        self.assertEqual(ba.users_id, usr.id)

        # MONEY
        # - is correctly set to default value 100
        self.assertEqual(ba.money, 100)