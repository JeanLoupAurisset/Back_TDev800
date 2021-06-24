from rest_framework import serializers
from .models import MeansOfPayment, BankAccount
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .configfile import limit_payment_trial, limit_amount

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'money', 'users_id')

    def validate_money(self, value):
        
        # Verify if bank account is blocked
        if self.instance.blocked == True:
            raise serializers.ValidationError("Your bank account is blocked")

        if value > limit_amount:
            raise serializers.ValidationError("The bill is too high")

        # Verify if there is enough money
        if value > self.instance.money:
            self.instance.count += 1 # increment the value count
            if self.instance.count >= limit_payment_trial:
                # bank account blocked
                self.instance.blocked = True
                self.instance.save()
                raise serializers.ValidationError("Your bank account has been blocked")
            self.instance.save()
            raise serializers.ValidationError("Not enough money")
        # If the operation succed then the count is set to 0
        self.instance.count = 0
        self.instance.save()
        return value

    def update(self, instance, validated_data):
        
        instance.money = instance.money - validated_data['money']
        instance.save()

        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username','password')
        extra_kwargs = {
            'username': {'validators': []},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data['username']

        instance.save()

        return instance
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        users_id = user.id
        obj = BankAccount.objects.create(**{'users_id':users_id})
        obj.save()

        return user

class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MeansOfPaymentSerializer(serializers.ModelSerializer):
    users_id = serializers.RelatedField(source='user', read_only=True)

    class Meta:
        model = MeansOfPayment
        fields = ('id','description','users_id')
    
    def create(self, validated_data):
        validated_data['users_id'] = self.context['request'].user.id
        obj = MeansOfPayment.objects.create(**validated_data)
        obj.save()
        return obj