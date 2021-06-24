from django.contrib import admin
from .models import MeansOfPayment, BankAccount

# Register your models here.

for model in [MeansOfPayment, BankAccount]:
    admin.site.register(model)
