from .test_setup import TestSetUp
from rest_framework import status as s
from API.models import Photo, User, Album
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




    def test_album_creation(self):

        # User creation
        userID = randint(1, 10)
        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # User getting
        usr = User.objects.get(id=userID)

        # album creation
        albumID = randint(1,10)
        album_data = {
            "Access_public": True,
            "description": "desc",
            "user_id": userID
        }
        Album.objects.create(id=albumID, name="desc", Access_public=True, user_id=album_data["user_id"])

        # album getting
        album = Album.objects.get(id=albumID)

        # USER ID
        # - is correct
        self.assertEqual(album.user_id, usr.id)

        # NAME
        # - is correct
        self.assertEqual(album.name, album.name)

        # ID
        # - id correct
        self.assertEqual(album.id, albumID)

    def test_photo_creation(self):
        # User creation
        userID = randint(1, 10)
        User.objects.create_user(id=userID, username=self.user_data["username"], email=self.user_data["email"],
                                 password=self.user_data["password"])

        # User getting
        usr = User.objects.get(id=userID)

        albumID = randint(1,10)
        album_data = {
            "Access_public": True,
            "description": "desc",
            "user_id": userID
        }
        Album.objects.create(id=albumID, name="desc", Access_public=True, user_id=album_data["user_id"])

        # photo creation
        photoID = randint(1,10)
        Photo.objects.create(id = photoID, name='test', album_id = albumID)

        # photo getting
        photo = Photo.objects.get(id = photoID)

        # ALBUM IS
        # - is correct
        self.assertEqual(photo.album_id, albumID)

        # NAME
        # - is correctly set to default value 100
        self.assertEqual(photo.name, 'test')