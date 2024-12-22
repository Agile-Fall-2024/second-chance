from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone_number', 'bio']


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'account']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        account_data = validated_data.pop('account', {})
        user = User.objects.create_user(**validated_data)
        Account.objects.create(user=user, **account_data)
        return user
