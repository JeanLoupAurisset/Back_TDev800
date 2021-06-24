from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BankAccount(models.Model):
    money = models.FloatField(default=100.0)
    count = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

class MeansOfPayment(models.Model):
    description = models.CharField(default='Card', max_length=100, unique=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description